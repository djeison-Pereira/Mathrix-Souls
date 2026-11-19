# Converte um .wav em .mp3 (128 kbps) usando o codificador do próprio Windows (sem instalar nada).
# Uso: powershell -NoProfile -File wav_para_mp3.ps1 origem.wav destino.mp3
param([string]$Origem, [string]$Destino)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$null = [Windows.Media.Transcoding.MediaTranscoder, Windows.Media.Transcoding, ContentType = WindowsRuntime]
$null = [Windows.Media.MediaProperties.MediaEncodingProfile, Windows.Media.MediaProperties, ContentType = WindowsRuntime]
$metodos = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 }
$asOp = $metodos | Where-Object { $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
$asAcao = $metodos | Where-Object { $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncActionWithProgress`1' } | Select-Object -First 1
function Esperar($op, $tipo) { $t = $asOp.MakeGenericMethod($tipo).Invoke($null, @($op)); $t.Wait(-1) | Out-Null; $t.Result }
$Origem = (Resolve-Path $Origem).Path
$Destino = [System.IO.Path]::GetFullPath($Destino)
if (Test-Path $Destino) { Remove-Item $Destino }
New-Item $Destino -ItemType File | Out-Null
$entrada = Esperar ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Origem)) ([Windows.Storage.StorageFile])
$saida = Esperar ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Destino)) ([Windows.Storage.StorageFile])
$perfil = [Windows.Media.MediaProperties.MediaEncodingProfile]::CreateMp3([Windows.Media.MediaProperties.AudioEncodingQuality]::Medium)
$tc = New-Object Windows.Media.Transcoding.MediaTranscoder
$prep = Esperar ($tc.PrepareFileTranscodeAsync($entrada, $saida, $perfil)) ([Windows.Media.Transcoding.PrepareTranscodeResult])
if (-not $prep.CanTranscode) { throw "O Windows não conseguiu preparar a conversão: $($prep.FailureReason)" }
$t = $asAcao.MakeGenericMethod([double]).Invoke($null, @($prep.TranscodeAsync()))
$t.Wait(-1) | Out-Null
