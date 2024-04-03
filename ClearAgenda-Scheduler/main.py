import tkinter as tk
from tkinter import ttk
from event import Event
from viewer import MonthViewer, WeekViewer
from memory import save_events_to_file,  load_events_from_file
from datetime import datetime, timedelta
from collections import defaultdict



events = defaultdict(list)
event_types = ["课程", "活动", "其他"]
root = tk.Tk()
events = load_events_from_file("events.json")
root.configure(background='white')

month_viewer = MonthViewer(root, events)
weekday_viewer = WeekViewer(root, events)

def input_event():
    window = tk.Toplevel(root)
    window.title("输入新活动")

    # 获取根窗口的位置和尺寸
    window_width = 400
    window_height = 200
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # 计算弹出窗口在屏幕上的位置以使其居中
    position_right = int(root_x + (root_width / 2) - (window_width / 2))
    position_down = int(root_y + (root_height / 2) - (window_height / 2))

    # 设置窗口的大小并且居中
    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")


    ttk.Label(window, text="事件名称").grid(row=0)
    ttk.Label(window, text="事件日期").grid(row=1)
    ttk.Label(window, text="开始时间").grid(row=2)
    ttk.Label(window, text="结束时间").grid(row=3)
    ttk.Label(window, text="事件类型").grid(row=4)  # 添加事件类型标签

    e1 = ttk.Entry(window)  # 事件名称
    e2 = ttk.Entry(window)  # 事件日期
    e3 = ttk.Entry(window)  # 开始时间
    e4 = ttk.Entry(window)  # 结束时间
    e5 = ttk.Combobox(window, values=event_types, state="readonly")  # 添加事件类型下拉列表
    e5.current(0)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)

    def submit():
        event_date = datetime.strptime(e2.get(), '%Y-%m-%d').date()
        start_time, end_time = datetime.strptime(e3.get(), '%H:%M').time(), datetime.strptime(e4.get(), '%H:%M').time()
        event = Event(name=e1.get(), event_date=event_date, start_time=start_time, end_time=end_time,
                      event_type=e5.get())
        events[event.event_date].append(event)

        save_events_to_file(events, "events.json")
        window.destroy()

        month_viewer.update_content(month_viewer.current_date.month, month_viewer.current_date.year)
        weekday_viewer.update_content(weekday_viewer.current_date)

    ttk.Button(window, text='提交', command=submit).grid(row=5)
# 周期性事件添加
def mul_input_event():
    window = tk.Toplevel(root)
    window.title("输入新活动")

    # 获取根窗口的位置和尺寸
    window_width = 400
    window_height = 230
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # 计算弹出窗口在屏幕上的位置以使其居中
    position_right = int(root_x + (root_width / 2) - (window_width / 2))
    position_down = int(root_y + (root_height / 2) - (window_height / 2))

    # 设置窗口的大小并且居中
    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")


    ttk.Label(window, text="事件名称").grid(row=0)
    ttk.Label(window, text="事件日期").grid(row=1)
    ttk.Label(window, text="开始时间").grid(row=2)
    ttk.Label(window, text="结束时间").grid(row=3)
    ttk.Label(window, text="事件类型").grid(row=4)  # 添加事件类型标签
    ttk.Label(window, text="事件周期").grid(row=5)
    ttk.Label(window, text="事件次数").grid(row=6)

    e1 = ttk.Entry(window)  # 事件名称
    e2 = ttk.Entry(window)  # 事件日期
    e3 = ttk.Entry(window)  # 开始时间
    e4 = ttk.Entry(window)  # 结束时间
    e5 = ttk.Combobox(window, values=event_types, state="readonly")  # 添加事件类型下拉列表
    e5.current(0)
    e6 = ttk.Entry(window)  # 事件周期
    e7 = ttk.Entry(window)  # 事件次数

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)
    e6.grid(row=5, column=1)
    e7.grid(row=6, column=1)

    def submit():
        for i in range(int(e7.get())):  # 注意这里将e7.get()转换为整数
            event_date = datetime.strptime(e2.get(), '%Y-%m-%d').date() + timedelta(
                days=int(e6.get()) * i)  # 注意这里将e6.get()转换为整数，并且每次循环递增
            start_time, end_time = datetime.strptime(e3.get(), '%H:%M').time(), datetime.strptime(e4.get(),
                                                                                                  '%H:%M').time()  # 注意这里将开始时间和结束时间转换为time对象
            event = Event(name=e1.get(),
                          event_date=event_date,
                          start_time=start_time,
                          end_time=end_time,
                          event_type=e5.get())
            events[event_date].append(event)

        save_events_to_file(events, "events.json")
        window.destroy()

        month_viewer.update_content(month_viewer.current_date.month, month_viewer.current_date.year)
        weekday_viewer.update_content(weekday_viewer.current_date)

    ttk.Button(window, text='提交', command=submit).grid(row=7)


def remove_event():
    window = tk.Toplevel(root)
    window.title("输入新活动")

    # 获取根窗口的位置和尺寸
    window_width = 400
    window_height = 200
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()

    # 计算弹出窗口在屏幕上的位置以使其居中
    position_right = int(root_x + (root_width / 2) - (window_width / 2))
    position_down = int(root_y + (root_height / 2) - (window_height / 2))

    # 设置窗口的大小并且居中
    window.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")


    ttk.Label(window, text="事件名称").grid(row=0)
    ttk.Label(window, text="事件日期").grid(row=1, column=0)

    e1 = ttk.Entry(window)  # 用户输入事件名称的地方
    e2 = ttk.Entry(window)  # 用户输入事件日期的地方

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    def submit():
        try:
            event_name = e1.get()
            event_date_str = e2.get()
            if event_date_str:  # 如果用户输入了日期
                event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
                # 只删除指定日期的事件
                events[event_date] = [event for event in events[event_date] if event.name != event_name]
            else:  # 如果用户没有输入日期
                # 删除所有日期中的指定名称的事件
                for date in list(events.keys()):
                    events[date] = [event for event in events[date] if event.name != event_name]

            # 保存更新后的事件
            save_events_to_file(events, "events.json")

            month_viewer.update_content(month_viewer.current_date.month, month_viewer.current_date.year)
            weekday_viewer.update_content(weekday_viewer.current_date)
        except ValueError:  # 如果日期格式错误就关闭界面
            window.destroy()

        window.destroy()

    ttk.Button(window, text='删除', command=submit).grid(row=2, columnspan=2)



def show_week():
    month_viewer.update_content(month_viewer.current_date.month, month_viewer.current_date.year)
    weekday_viewer.update_content(weekday_viewer.current_date)
    month_viewer.frame.place_forget()
    weekday_viewer.frame.place(x=50, y=50, width=1000, height=520)

def show_month():
    month_viewer.update_content(month_viewer.current_date.month, month_viewer.current_date.year)
    weekday_viewer.update_content(weekday_viewer.current_date)
    weekday_viewer.frame.place_forget()
    month_viewer.frame.place(x=50, y=50, width=1000, height=520)

# 你其余的代码



button_week = ttk.Button(root, text="显示星期", command=show_week)
button_week.place(x=50, y=10, width=120, height=30)

button_month = ttk.Button(root, text="显示月份", command=show_month)
button_month.place(x=200, y=10, width=120, height=30)

button_input = ttk.Button(root, text="输入新活动", command=input_event)
button_input.place(x=400, y=10, width=120, height=30)


button_mul_input_event = ttk.Button(root, text="周期添加", command=mul_input_event)
button_mul_input_event.place(x=600, y=10, width=120, height=30)


button_remove = ttk.Button(root, text="删除活动", command=remove_event)
button_remove.place(x=800, y=10, width=120, height=30)


root.minsize(1100, 600)
root.maxsize(1100, 600)
show_week()
root.mainloop()