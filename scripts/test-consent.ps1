<#
.SYNOPSIS
  Test the Consent Lambda webhook from PowerShell (opt-in, opt-out, status).

.DESCRIPTION
  Sends a request to the Consent Function URL either as a Twilio-style form POST
  (JOIN MITZVAH / STOP / STATUS) or as a JSON web opt-in/out.
  Optionally verifies the resulting record in DynamoDB.

.REQUIREMENTS
  - AWS CLI configured with credentials and default region OR pass -Region
  - PowerShell 5.1+

.EXAMPLES
  # Opt-in via Twilio-style message (JOIN MITZVAH)
  ./scripts/test-consent.ps1 -Phone "+1YOURNUMBER" -Action optin

  # Opt-out via STOP
  ./scripts/test-consent.ps1 -Phone "+1YOURNUMBER" -Action optout

  # Query status
  ./scripts/test-consent.ps1 -Phone "+1YOURNUMBER" -Action status

  # Use a custom Twilio To number
  ./scripts/test-consent.ps1 -Phone "+1YOURNUMBER" -Action optin -TwilioTo "+14155238886"

  # Web JSON opt-in (no Twilio fields)
  ./scripts/test-consent.ps1 -Phone "+1YOURNUMBER" -Action web-optin

  # Verify DynamoDB after sending
  ./scripts/test-consent.ps1 -Phone "+1YOURNUMBER" -Action optin -Verify

.PARAMETER Phone
  E.164 phone like +1XXXXXXXXXX (no whatsapp: prefix). Required.

.PARAMETER Action
  One of: optin | optout | status | web-optin | web-optout (default: optin)

.PARAMETER TwilioFrom
  Optional override of From; defaults to whatsapp:<Phone> for Twilio-style actions.

.PARAMETER TwilioTo
  Twilio destination number (E.164). Will be prefixed with whatsapp: for Twilio-style actions.
  Default: +14155238886

.PARAMETER StackName
  CloudFormation stack name used during deploy. Default: daily-mitzvah-bot-stack

.PARAMETER Region
  AWS region (falls back to $env:AWS_REGION or $env:AWS_DEFAULT_REGION).

.PARAMETER ConsentUrl
  Override the Consent Function URL directly. If not provided, resolved from CFN outputs.

.PARAMETER Verify
  If set, query DynamoDB to print the subscriber record after the call.
#>

param(
  [Parameter(Mandatory=$true)]
  [string]$Phone,

  [ValidateSet('optin','optout','status','web-optin','web-optout')]
  [string]$Action = 'optin',

  [string]$TwilioFrom,
  [string]$TwilioTo = '+14155238886',

  [string]$StackName = 'daily-mitzvah-bot-stack',
  [string]$Region,
  [string]$ConsentUrl,

  [switch]$Verify,
  [switch]$OnlyVerify,
  [switch]$VerboseLogs
)

# Resolve region from environment if not provided
if (-not $Region -or $Region -eq '') {
  if ($env:AWS_REGION -and $env:AWS_REGION -ne '') { $Region = $env:AWS_REGION }
  elseif ($env:AWS_DEFAULT_REGION -and $env:AWS_DEFAULT_REGION -ne '') { $Region = $env:AWS_DEFAULT_REGION }
}
if (-not $Region -or $Region -eq '') {
  Write-Error "No AWS region found. Set -Region or configure AWS_REGION/AWS_DEFAULT_REGION."
  exit 1
}

function Get-ConsentUrl {
  param(
    [string]$StackName,
    [string]$Region
  )
  try {
    $url = aws cloudformation describe-stacks --stack-name $StackName --query "Stacks[0].Outputs[?OutputKey=='ConsentFunctionUrl'].OutputValue" --output text --region $Region 2>$null
    if (-not $url -or $url -eq 'None') { return $null }
    $url = $url.Trim()

    # If the output is an ARN (older stack output), try to resolve the Function URL via Lambda API
    if ($url -notmatch '^https?://') {
      if ($url -match '^arn:aws:lambda:[^:]+:\d{12}:function:(?<fn>[^:]+)$') {
        $fnName = $Matches['fn']
        try {
          $fnUrl = aws lambda get-function-url-config --function-name $fnName --region $Region --query 'FunctionUrl' --output text 2>$null
          if ($fnUrl -and $fnUrl -ne 'None') { return $fnUrl.Trim() }
        } catch {}
      }
      # Not a URL and couldn't resolve; return null to force explicit override
      return $null
    }
    return $url
  } catch {
    return $null
  }
}

function Get-SubscribersTableName {
  param(
    [string]$StackName
  )
  # Matches template.yaml: TableName: "${AWS::StackName}-subscribers"
  return "$StackName-subscribers"
}

function UrlEncode($s) { return [System.Uri]::EscapeDataString([string]$s) }

function Invoke-TwilioStyle {
  param(
    [string]$ConsentUrl,
    [string]$From,
    [string]$To,
    [string]$Body
  )
  $form = "From=$(UrlEncode $From)&To=$(UrlEncode $To)&Body=$(UrlEncode $Body)"
  if ($VerboseLogs) { Write-Host "POST $ConsentUrl`n$form" }
  return Invoke-RestMethod -Uri $ConsentUrl -Method Post -ContentType 'application/x-www-form-urlencoded' -Body $form
}

function Invoke-WebJson {
  param(
    [string]$ConsentUrl,
    [string]$Phone,
    [string]$Action,
    [bool]$Consent
  )
  # PowerShell 5.1 doesn't support the C#-style ternary operator
  $consentStr = if ($Consent) { 'true' } else { 'false' }
  $payload = @{ phone = $Phone; action = $Action; consent = $consentStr } | ConvertTo-Json -Depth 3
  if ($VerboseLogs) { Write-Host "POST $ConsentUrl`n$payload" }
  return Invoke-RestMethod -Uri $ConsentUrl -Method Post -ContentType 'application/json' -Body $payload
}

function Verify-Ddb {
  param(
    [string]$Region,
    [string]$Table,
    [string]$Phone
  )
  $key = @{ phone = @{ S = $Phone } } | ConvertTo-Json -Compress
  $tmp = New-TemporaryFile
  # Write UTF-8 without BOM for AWS CLI JSON parsing compatibility on Windows PowerShell 5.1
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($tmp.FullName, $key, $utf8NoBom)
  $raw = aws dynamodb get-item --table-name $Table --key file://$($tmp.FullName) --region $Region | Out-String
  Remove-Item -Path $tmp -Force -ErrorAction SilentlyContinue
  Write-Host "DynamoDB get-item result:" -ForegroundColor Cyan
  Write-Host $raw
}

# Resolve Consent URL if not explicitly provided
if (-not $ConsentUrl -or $ConsentUrl -eq '') {
  $ConsentUrl = Get-ConsentUrl -StackName $StackName -Region $Region
  if (-not $ConsentUrl) {
    Write-Error "Could not resolve Consent Function URL from stack '$StackName' in region '$Region'. Pass -ConsentUrl explicitly."
    exit 2
  }
}

# If we only want to verify DynamoDB without sending a request
if ($OnlyVerify) {
  $table = Get-SubscribersTableName -StackName $StackName
  Verify-Ddb -Region $Region -Table $table -Phone $Phone
  exit 0
}

# Compose Twilio From/To for Twilio-style actions
$twilioActions = @('optin','optout','status')
if ($twilioActions -contains $Action) {
  if (-not $TwilioFrom -or $TwilioFrom -eq '') { $TwilioFrom = "whatsapp:$Phone" }
  if ($TwilioTo -notmatch '^whatsapp:') { $TwilioTo = "whatsapp:$TwilioTo" }
}

# Dispatch
try {
  switch ($Action) {
    'optin' {
      $resp = Invoke-TwilioStyle -ConsentUrl $ConsentUrl -From $TwilioFrom -To $TwilioTo -Body 'JOIN MITZVAH'
    }
    'optout' {
      $resp = Invoke-TwilioStyle -ConsentUrl $ConsentUrl -From $TwilioFrom -To $TwilioTo -Body 'STOP'
    }
    'status' {
      $resp = Invoke-TwilioStyle -ConsentUrl $ConsentUrl -From $TwilioFrom -To $TwilioTo -Body 'STATUS'
    }
    'web-optin' {
      $resp = Invoke-WebJson -ConsentUrl $ConsentUrl -Phone $Phone -Action 'optin' -Consent $true
    }
    'web-optout' {
      $resp = Invoke-WebJson -ConsentUrl $ConsentUrl -Phone $Phone -Action 'optout' -Consent $false
    }
  }
  Write-Host "Response:" -ForegroundColor Green
  $resp | Out-String | Write-Host
} catch {
  Write-Error "Request failed: $($_.Exception.Message)"
  exit 3
}

# Optional verification in DynamoDB
if ($Verify) {
  $table = Get-SubscribersTableName -StackName $StackName
  Verify-Ddb -Region $Region -Table $table -Phone $Phone
}
