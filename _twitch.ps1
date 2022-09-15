# 
# Robin's start streamlink script
# new-item -path .\lirik.ps1 -ItemType HardLink -value .\_twitch.ps1

# get script file filename
$filename = $MyInvocation.MyCommand.Name
# remove file extension
$streamer = $filename.split(".")[0]
Write-Output("> Attemping to view " + $streamer +" on twitch.tv ...")
streamlink twitch.tv/$streamer best
