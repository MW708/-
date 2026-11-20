def main():
    MAX_NAMES = 300
    MAX_NAME_LENGTH = 50
    
    #print("请输入姓名，用空格分隔，最多300个，输入\"end\"结束：")
    print("请输入姓名，用顿号分隔，最多300个，输入\"end\"结束：")
    
    # 读取一行输入
    input_line = input().strip()
    
    # 按空格分割姓名
    # all_names = input_line.split()

    # 按、分隔姓名
    all_names = input_line.split('、')
    
    # 处理结束标志并限制最大数量
    names = []
    for name in all_names:
        if name.lower() == "end":
            break
        if len(names) >= MAX_NAMES:
            break
        # 限制姓名长度
        if len(name) > MAX_NAME_LENGTH:
            name = name[:MAX_NAME_LENGTH]
        names.append(name)
    
    total_names = len(names)
    
    # 统计每个姓名的出现次数
    name_counts = {}
    for name in names:
        if name in name_counts:
            name_counts[name] += 1
        else:
            name_counts[name] = 1
    
    # 按重复次数降序排列
    sorted_names = sorted(
        name_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # 打印所有姓名及其出现次数（按重复次数降序）
    print("\n所有姓名统计结果（按出现次数降序排列）：")
    print("====================")
    
    for name, count in sorted_names:
        status = "重复" if count > 1 else "唯一"
        print(f"姓名: {name.ljust(20)} 出现次数: {count} ({status})")
    
    # 计算重复和唯一的姓名数量
    duplicate_count = sum(1 for _, count in name_counts.items() if count > 1)
    unique_count = len(name_counts) - duplicate_count
    
    # 打印统计摘要
    print("\n统计摘要：")
    print(f"总姓名数: {total_names}")
    print(f"唯一姓名数: {unique_count}")
    print(f"重复姓名数: {duplicate_count}")
    print(f"重复姓名种类: {duplicate_count} 种")

if __name__ == "__main__":
    main()
    
"MW_Sparks"