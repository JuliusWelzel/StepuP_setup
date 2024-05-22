# Setup software

# LabRecorder config file
Please add this to the config file witht he correct dir for data storage
```
; === Set directories ===
StudyRoot=${StudyRootDir}/data/
PathTemplate=sub-%p_ses-%s_task-%b_eeg.xdf

; === Block Names ===
SessionBlocks="ComfortableSpeed", "FixedSpeed", "RestingState" 
```