# 自动化设备管理平台

## 需求

1. 设备信息添加
- 设备IP
- 设备名称
- 设备版本
- 工装设备IP
- 工装电脑IP
- 每日编译状态「只读」
> 修改时间大于x天自动释放

- 设备使用状态「只读」
- 设备SD卡状态
- 设备位置
- 添加时间
- 修改时间「不可见」
- 逻辑删除「不可见」
2. 获取空闲设备

- 输入`设备IP`返回使用状态
- 输入`设备名称`返回使用状态
- 输入`测试类型`「每日编译/正式版本/工装」返回空闲设备列表
3. 修改使用状态
- 使用`设备IP`+`使用状态`来进行修改


