# esp8266_led_demo
通过浏览器控制ESP8266上的LED

参考:
This is example code for [this blog post](http://jpmens.net/2014/07/03/the-mosquitto-mqtt-broker-gets-websockets-support/).

    如何通过浏览器控制ESP8266?这里提供一个方法。可以用mq消息机制，通过消息的方法专递信息给esp8266。原理是浏览器通过websocket接口连接mq服务器，再点击on/off按钮之后发送消息给mq服务器，mq服务器接受到消息之后通过micropython的mqtt库程序将消息传递给esp8266，根据消息内容来打开或者关闭esp8266上的led。
一、安装mosquitto（在linux环境下）</br>

    mosquitto默认安装不支持websocket，需以下步骤安装</br>
 	1、下载mosquitto、libwebsockets、cmake</br>
 	wget http://mosquitto.org/files/source/mosquitto-1.4.12.tar.gz</br>
 	tar -zxvf mosquitto-1.4.12.tar.gz</br>
 	useradd mosquitto #需要新建一个用户</br>
 	git clone https://github.com/warmcat/libwebsockets</br>
	编译需要cmake</br>
	所以：apt-get install cmake</br>
	2、安装</br>
	完成以后 进入libwebsockets目录</br>
	mkdir build</br>
	cd build</br>
	cmake .. -DOPENSSL_ROOT_DIR=/usr/bin/openssl</br>
	make</br>
	sudo make install</br>
	进入mosquitto目录</br>
	更改configure.mk中WITH_WEBSOCKETS:=no变成（这一步是做WebSocket支持）WITH_WEBSOCKETS:=yes</br>
	修改配置，编译。</br>
	make</br>
	make install</br>
	启动：mosquitto -c /etc/mosquitto/mosquitto.conf </br>
	有可能找不到动态库，查一下库文件目录，并确保动态库在/etc/ld.so.conf</br>
	mosquitto安装注意点</br>
	【1】编译找不到openssl/ssl.h</br>
	 安装openssl</br>
	sudo apt-get install libssl-dev</br>
	【2】编译过程找不到ares.h</br>
	sudo apt-get install libc-ares-dev</br>
	【3】编译过程找不到uuid/uuid.h</br>
	sudo apt-get install uuid-dev</br>
	【4】使用过程中找不到libmosquitto.so.1</br>
	error while loading shared libraries: libmosquitto.so.1: cannot open shared object file: No such file or directory</br>
	修改libmosquitto.so位置</br>
	# 创建链接</br>
	sudo ln -s /usr/local/lib/libmosquitto.so.1 /usr/lib/libmosquitto.so.1</br>
	# 更新动态链接库</br>
	sudo ldconfig</br>
	【5】make: g++：命令未找到</br>
	 装g++编译器</br>
	sudo apt-get install g++</br>

二、安装tornado</br>
	sudo pip install tornado</br>

三、下载源代码并测试</br>
	git clone https://github.com/breezecloud/esp8266_led_demo.git或者到 https://github.com/breezecloud/esp8266_led_demo直接下载</br>
	led_mqtt.py #ESP8266执行程序</br>
	websocket_led.py #命令行启动tornado程序</br>
	templates--index.html #web页面</br>
	static/scripts--config.js,jquery.min.js,mqttws31.js #javascript库</br>
	esp8266安装micropython的固件（参考http://blog.sina.com.cn/s/blog_537da9e40102x79k.html）</br>
	修改led_mqtt.py中ap的ssid和密码，并上传到esp8266(参考http://blog.sina.com.cn/s/blog_537da9e40102x83s.html)</br>
	然后登录esp8266，执行import led_mqtt.py。此时可以在linux终端上执行mosquitto_pub -t '/esp8266' -m on和mosquitto_pub -t '/esp8266' -m off测试esp8266是否正常工作</br>
	在linux终端下执行pythhon websocket_led.py。浏览器http://ip地址:8000（注意：必须支持websocket的浏览器），点击上面的on/off按钮控制led的亮和暗。</br>
这样一个mini物联网完成了。</br>
