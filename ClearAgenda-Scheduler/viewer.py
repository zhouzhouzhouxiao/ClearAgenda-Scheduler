import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from collections import defaultdict
from memory import save_events_to_file

class ToolTip:
    def __init__(self, widget):
        self.waittime = 100
        self.wraplength = 180
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{int(x)}+{int(y)}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="white", relief=tk.SOLID, borderwidth=1, wraplength=self.wraplength)
        label.pack()

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def set_text(self, text):
        self.text = text


class MonthViewer:
    def __init__(self, master, events):
        self.events = events
        self.master = master
        self.frame = ttk.Frame(self.master, padding="10")
        self.current_date = datetime.now()
        self.num_days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self.current_date.year % 4 == 0:
            if self.current_date.year % 100 != 0 or self.current_date.year % 400 == 0:
                self.num_days_in_month[1] = 29
        self.day_labels = [ttk.Label(self.frame, text=day, width=10, font=('Helvetica', 14)) for day in ['周日', '周一', '周二', '周三', '周四', '周五', '周六']]
        for i, label in enumerate(self.day_labels):
            label.place(x=140*i+30, y=60)

        # 创建一个 Frame 的列表（label_frames）来包装每个日期标签
        self.label_frames = []
        for i in range(42):
            # 使用 Frame widget 作为每个日期标签的容器
            frame = tk.Frame(self.frame, width=140, height=90)
            frame.place(x=140*(i%7)-8, y=90+90*(i//7))
            frame.pack_propagate(0)  # 不允许 Frame 改变大小以适应其内容
            self.label_frames.append(frame)

        self.update_content(self.current_date.month, self.current_date.year)
        prev_button = ttk.Button(self.frame, text='上一月', command=self.prev_month)
        next_button = ttk.Button(self.frame, text='下一月', command=self.next_month)
        prev_button.place(x=0, y=0)
        next_button.place(x=200, y=0)

    def update_content(self, month, year):
        first_day_of_month = datetime(year, month, 1)
        last_day_of_month = first_day_of_month + timedelta(days=self.num_days_in_month[month - 1] - 1)
        start_day = first_day_of_month - timedelta(days=(first_day_of_month.weekday() + 1) % 7)
        end_day = last_day_of_month + timedelta(days=(6 - last_day_of_month.weekday()))

        for i, frame in enumerate(self.label_frames):
            current_day = start_day + timedelta(days=i)

            # 清空frame
            for widget in frame.winfo_children():
                widget.destroy()

            # 仅为当前月份创建日期标签
            if first_day_of_month <= current_day <= last_day_of_month:
                event_date = current_day.date()
                events_on_date = self.events.get(event_date, [])
                event_count = len(events_on_date)
                # 以下代码修正了之前的问题，现在将显示完整的日期
                label_text = f"{current_day.strftime('%Y-%m-%d')}\n{event_count}     "
                label = tk.Label(frame, text=label_text, font=("Helvetica", 14))
                label.pack()

                if event_count > 0:
                    tooltip = ToolTip(frame)
                    event_text = '\n'.join(str(event) for event in events_on_date)
                    tooltip.set_text(event_text)


        self.current_date = first_day_of_month

    def prev_month(self):
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.update_content(self.current_date.month, self.current_date.year)

    def next_month(self):
        self.current_date = self.current_date.replace(day=1) + timedelta(days=self.num_days_in_month[self.current_date.month - 1])
        self.update_content(self.current_date.month, self.current_date.year)


class WeekViewer:
    def __init__(self, master, events):
        self.events = events
        self.frame = ttk.Frame(master, padding="10")
        self.days_of_week = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
        # labels for days of week
        self.day_labels = [ttk.Label(self.frame, text=day, width=10, font=('Helvetica', 14)) for day in self.days_of_week]
        # labels for dates
        self.labels = [ttk.Label(self.frame, width=10, font=('Helvetica', 14)) for _ in range(7)]
        for i, day_label in enumerate(self.day_labels):
            day_label.place(x=140*i+30, y=60)
        for i, label in enumerate(self.labels):
            label.place(x=140*i, y=90)
        self.current_date = datetime.now()
        self.event_labels = []
        self.update_content(self.current_date)
        prev_button = ttk.Button(self.frame, text='上一周', command=self.prev_week)
        next_button = ttk.Button(self.frame, text='下一周', command=self.next_week)
        prev_button.place(x=0, y=0)
        next_button.place(x=200, y=0)

    def time_to_pos(self, time):
        return 20 * (time.hour + time.minute / 60)

    def update_content(self, date_in_week):

        for label in self.event_labels:  # 在创建新标签之前，删除旧的事件标签
            label.destroy()
        self.event_labels = []


        start_date = date_in_week - timedelta(days=(date_in_week.weekday() + 1) % 7)
        label_x_offsets = defaultdict(int)

        for i, date_label in enumerate(self.labels):  # change 'day_labels' to 'labels'
            date = start_date + timedelta(days=i)
            date_label['text'] = f'{date.strftime("%Y-%m-%d")}'

            for event in sorted(self.events.get(date.date(), []), key=lambda e: e.start_time):
                start_y = self.time_to_pos(event.start_time)
                end_y = self.time_to_pos(event.end_time)

                label = tk.Label(self.frame, text=event.name, bg="green", width=8)
                label.place(x=140 * i+22, y=start_y, height=end_y - start_y)
                label_x_offsets[date] += 10
                label.bind('<Button-3>',
                           lambda e, lbl=label, evt=event: self.show_right_click_menu(lbl, evt, e.x_root, e.y_root))
                self.event_labels.append(label)

    # 这个方法用于创建并显示右键菜单
    def show_right_click_menu(self, event_label, event, x, y):
        # 创建一个菜单
        popup_menu = tk.Menu(self.frame, tearoff=0)
        # 添加一个 'Delete' 选项，绑定到 delete_event 方法
        popup_menu.add_command(
            label='删除',
            command=lambda: self.delete_event(event, event_label)
        )
        # 显示菜单
        popup_menu.tk_popup(x, y)

    # 实现删除事件的具体方法
    def delete_event(self, event, event_label):
        # 移除事件
        self.events[event.event_date].remove(event)
        # 从界面上移除事件的标签
        event_label.destroy()
        # 更新文件中的事件列表
        save_events_to_file(self.events, "events.json")
        self.update_content(self.current_date)
    # 修改 update_content 方法中创建事件标签的部分



    def prev_week(self):
        self.current_date -= timedelta(weeks=1)
        self.update_content(self.current_date)

    def next_week(self):
        self.current_date += timedelta(weeks=1)
        self.update_content(self.current_date)
