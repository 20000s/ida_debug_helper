每次调试apk so文件前的前置工作太麻烦了 adb forward  jdb 啥的 还要一直f9 到所调试的so加载进内存，
于是写了个脚本，自动化完成调试的前置工作，直接运行到所需的so文件load,帮助逆向者抛开前面的繁琐工作

#requiment:
1. python3
2. [adbutils](https://github.com/openatx/adbutils)


#usage:
1.手机上运行ida的android_server
2. ida载入脚本 运行start_debug(package_name,so_name) 所调试的apk名字 so的名字 
3. 按照脚本提示 手机上点击一次apk
即可完整

# 【todo】
打算做个idapython脚本汇总，将可能用到的功能包含进去
1. dump (done)  dump(start_address,end_address)
2. break jni_onload
3. break init_array


