
import random

def lottery():
    print("=" * 40)
    print("          Python 随机抽签工具")
    print("=" * 40)

    # 输入参与抽签的人员
    names_input = input("请输入参与抽签的人员姓名（用逗号隔开）：")
    names = [name.strip() for name in names_input.split(",") if name.strip()]

    if not names:
        print("名单不能为空！")
        return

    # 去除重复姓名
    names = list(dict.fromkeys(names))

    remaining_names = names.copy()
    winners = []

    print(f"\n当前共有 {len(names)} 人参与抽签。")

    while remaining_names:
        print("\n请选择操作：")
        print("1. 抽取一人")
        print("2. 抽取指定人数")
        print("3. 查看已中奖名单")
        print("4. 查看剩余名单")
        print("5. 退出程序")

        choice = input("\n请输入选项：").strip()

        if choice == "1":
            winner = random.choice(remaining_names)
            remaining_names.remove(winner)
            winners.append(winner)

            print("\n🎉 恭喜中奖！")
            print(f"中奖人员：{winner}")

        elif choice == "2":
            try:
                count = int(input("请输入抽取人数："))

                if count <= 0:
                    print("抽取人数必须大于0！")
                elif count > len(remaining_names):
                    print(f"剩余人数只有 {len(remaining_names)} 人，无法抽取！")
                else:
                    selected = random.sample(remaining_names, count)

                    for name in selected:
                        remaining_names.remove(name)
                        winners.append(name)

                    print("\n🎉 本次中奖名单：")
                    for i, name in enumerate(selected, 1):
                        print(f"{i}. {name}")

            except ValueError:
                print("请输入有效的整数！")

        elif choice == "3":
            print("\n已中奖名单：")
            if winners:
                for i, name in enumerate(winners, 1):
                    print(f"{i}. {name}")
            else:
                print("暂时还没有人中奖。")

        elif choice == "4":
            print("\n剩余参与人员：")
            for i, name in enumerate(remaining_names, 1):
                print(f"{i}. {name}")

        elif choice == "5":
            print("\n抽签结束！")
            print(f"参与人数：{len(names)}")
            print(f"中奖人数：{len(winners)}")
            print("最终中奖名单：", winners)
            break

        else:
            print("输入错误，请重新选择！")

    if not remaining_names:
        print("\n所有人员均已抽取完毕！")
        print("最终中奖名单：", winners)


if __name__ == "__main__":
    lottery()
