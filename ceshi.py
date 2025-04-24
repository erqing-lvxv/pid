from configparser import RawConfigParser

# 读取配置文件
config = RawConfigParser()
config.read('config.ini', encoding='utf-8')

# 从配置文件中获取counter的值，如果不存在则设置为0
counter = int(config.get('settings', 'counter', fallback=0))
agent = str(config.get('settings', 'agent', fallback=0))
cookie = str(config.get('settings', 'cookie', fallback=0))

# 更新counter的值
counter += 1
cookie = 567
# 输出counter的值
print(counter)
print(agent)
print(cookie)

# 保存counter的值到配置文件
config['settings']['counter'] = str(counter)
config['settings']['cookie'] = str(cookie)
with open('config.ini', 'w') as configfile:
    config.write(configfile)