# Introduction
TODO

## References
- [React Native WSL2 Setup](https://gist.github.com/bergmannjg/461958db03c6ae41a66d264ae6504ade)

# Setup
TODO
NOTE - On windows 10, internet connectivity fails for emulator API versions above 29
React Native does not support symlinks - have to use a workaround for shard libraries: https://medium.com/@slavik_210/symlinks-on-react-native-ae73ed63e4a7

loading to phone - https://reactnative.dev/docs/running-on-device

# Run
```
# run each line in different sessions :(
# windows - start emulator and start adb server
cd ~/AppData/Local/Android/Sdk/emulator ; .\emulator.exe -avd Pixel_2_API_33
adb kill-server ; adb -a nodaemon server start

# wsl2 - setup adb connectivity, start bundling server, and run the final thing
socat -d -d TCP-LISTEN:5037,reuseaddr,fork TCP:$(cat /etc/resolv.conf | tail -n1 | cut -d " " -f 2):5037
npx react-native start --host 127.0.0.1
npx react-native run-android --variant=debug --deviceId emulator-5554
```

## installing on physical device
- TODO I think the adb installed on wsl is busted, things don't seem to work unless I point to the one on windows: `/mnt/c/Users/Bieni/AppData/Local/Android/Sdk/platform-tools/adb.exe`
- still very unclear on how to use this guide, [React Native on Mobile Guide](https://reactnative.dev/docs/running-on-device)
- it seems that, when running over USB, I need to run metro with `npx react-native start --host 127.0.0.1` (make sure host arg is provided) - this isn't mentioned in the guide