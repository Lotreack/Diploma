import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):

        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_open_dialog = tk.Button(
            toolbar,
            text="Добавить данные",
            command=self.open_dialog,
            bg="#d7d8e0",
            bd=2,
            compound=tk.TOP,
            image=self.add_img,
        )
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file="./img/edit.png")
        btn_edit_dialog = tk.Button(
            toolbar,
            text="Редактировать",
            bg="#d7d8e0",
            bd=2,
            image=self.update_img,
            compound=tk.TOP,
            command=self.open_update_dialog,
        )
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file="./img/delete.png")
        btn_delete_dialog = tk.Button(
            toolbar,
            text="Удалить запись",
            bg="#d7d8e0",
            bd=2,
            image=self.delete_img,
            compound=tk.TOP,
            command=self.delete_records,
        )
        btn_delete_dialog.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")
        btn_refresh_dialog = tk.Button(
            toolbar,
            text="Обновить",
            bg="#d7d8e0",
            bd=2,
            image=self.refresh_img,
            compound=tk.TOP,
            command=self.view_records,
        )
        btn_refresh_dialog.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file="./img/search.png")
        btn_search_dialog = tk.Button(
            toolbar,
            text="Найти запись",
            bg="#d7d8e0",
            bd=2,
            image=self.search_img,
            compound=tk.TOP,
            command=self.open_search_dialog,
        )
        btn_search_dialog.pack(side=tk.LEFT)

        self.search_img_link = tk.PhotoImage(file="./img/search_link.png")
        btn_search_link_dialog = tk.Button(
            toolbar,
            text="Найти запись по ссылке",
            bg="#d7d8e0",
            bd=2,
            image=self.search_img_link,
            compound=tk.TOP,
            command=self.open_search_link_dialog,
        )
        btn_search_link_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self,
            columns=(
                "ID",
                "Description",
                "Type",
                "Activity",
                "Link",
                "Author",
                "Comments",
                "Risk",
            ),
            height=15,
            show="headings",
        )

        self.tree.column("ID", width=70, anchor=tk.CENTER)
        self.tree.column("Description", width=300, anchor=tk.CENTER)
        self.tree.column("Type", width=150, anchor=tk.CENTER)
        self.tree.column("Activity", width=180, anchor=tk.CENTER)
        self.tree.column("Link", width=120, anchor=tk.CENTER)
        self.tree.column("Author", width=150, anchor=tk.CENTER)
        self.tree.column("Comments", width=250, anchor=tk.CENTER)
        self.tree.column("Risk", width=250, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID записи")
        self.tree.heading(
            "Description",
            text="Описание контента",
        )
        self.tree.heading("Type", text="Тип контента")
        self.tree.heading("Activity", text="Количество просмотров")
        self.tree.heading("Link", text="Ссылка на контент")
        self.tree.heading(
            "Author",
            text="Автор поста",
        )

        self.tree.heading("Comments", text="Количество комментариев")

        self.tree.heading("Risk", text="Риск распростарнения контента")

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def record(
        self, description, type, activity, link, author, comments, risk
    ):
        self.db.insert_data(
            description, type, activity, link, author, comments, risk
        )
        self.view_records()

    def update_record(
        self, description, type, activity, link, author, comments, risk
    ):
        self.db.curs.execute(
            """UPDATE destructive_content SET description=?, type=?, activity=?, link=?, author=?, comments=?, risk=? WHERE ID=?""",
            (
                description,
                type,
                activity,
                link,
                author,
                comments,
                risk,
                self.tree.set(self.tree.selection()[0], "#1"),
            ),
        )
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.curs.execute("""SELECT * FROM destructive_content""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [
            self.tree.insert("", "end", values=row)
            for row in self.db.curs.fetchall()
        ]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.curs.execute(
                """DELETE FROM destructive_content WHERE id=?""",
                (self.tree.set(selection_item, "#1"),),
            )
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ("%" + description + "%",)
        self.db.curs.execute(
            """SELECT * FROM destructive_content WHERE description LIKE ?""",
            description,
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [
            self.tree.insert("", "end", values=row)
            for row in self.db.curs.fetchall()
        ]

    def search_link_records(self, link):
        link = ("%" + link + "%",)
        self.db.curs.execute(
            """SELECT * FROM destructive_content WHERE link LIKE ?""",
            link,
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [
            self.tree.insert("", "end", values=row)
            for row in self.db.curs.fetchall()
        ]

    def open_dialog(self):
        Child_add()

    def open_update_dialog(self):
        Child_update()

    def open_search_dialog(self):
        Search()

    def open_search_link_dialog(self):
        Search_link()


class Child_add(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Добавить данные о контенте")
        self.geometry("800x400+400+300")
        self.resizable(True, True)
        ########################################################

        label_description = tk.Label(self, text="Наименование")
        label_description.place(x=120, y=110)

        label_type = tk.Label(self, text="Тип")
        label_type.place(x=120, y=140)

        label_activity = tk.Label(self, text="Количество переходов к посту")
        label_activity.place(x=120, y=170)

        label_link = tk.Label(self, text="Ссылка на пост")
        label_link.place(x=120, y=200)

        label_author = tk.Label(self, text="Автор")
        label_author.place(x=120, y=230)

        label_comments = tk.Label(self, text="Количество комментариев")
        label_comments.place(x=120, y=260)

        # label_risk = tk.Label(self, text="Риск")
        # label_risk.place(x=120, y=290)
        ########################################################

        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=300, y=110)

        self.entry_type = self.combobox = ttk.Combobox(
            self,
            values=[
                u"Видео",
                u"Картинка",
                u"Текстовый пост",
                u"Ссылка",
                u"Текстовый комментарий",
            ],
        )
        self.combobox.current(0)
        self.combobox.place(x=300, y=140)

        self.entry_activity = ttk.Entry(self)
        self.entry_activity.place(x=300, y=170)

        self.entry_link = ttk.Entry(self)
        self.entry_link.place(x=300, y=200)

        self.entry_author = ttk.Entry(self)
        self.entry_author.place(x=300, y=230)

        self.entry_comments = ttk.Entry(self)
        self.entry_comments.place(x=300, y=260)

        # self.entry_risk = ttk.Entry(self)
        # self.entry_risk.place(x=300, y=290)
        ###############################################################

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=720, y=370)

        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=720, y=10)
        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.record(
                self.entry_description.get(),
                self.entry_type.get(),
                self.entry_activity.get(),
                self.entry_link.get(),
                self.entry_author.get(),
                self.entry_comments.get(),
                float(self.entry_activity.get())
                * float(self.entry_comments.get())
                * 0.0000001,
            ),
        )

        self.grab_set()
        self.focus_set()


class Child_update(Child_add):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title("Редактировать запись")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=700, y=30)
        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_record(
                self.entry_description.get(),
                self.entry_type.get(),
                self.entry_activity.get(),
                self.entry_link.get(),
                self.entry_author.get(),
                self.entry_comments.get(),
                float(self.entry_activity.get())
                * float(self.entry_comments.get())
                * 0.0000001,
            ),
        )
        self.btn_ok.destroy()

    def default_data(self):
        self.db.curs.execute(
            """SELECT * FROM destructive_content WHERE id=?""",
            (self.view.tree.set(self.view.tree.selection()[0], "#1"),),
        )
        row = self.db.curs.fetchone()
        self.entry_description.insert(0, row[1])
        self.entry_type.insert(0, row[2])
        if row[2] == "Видео":
            self.combobox.current(0)
        elif row[2] == "Картинка":
            self.combobox.current(1)
        elif row[2] == "Текстовый пост":
            self.combobox.current(2)
        elif row[2] == "Ссылка":
            self.combobox.current(3)
        self.entry_activity.insert(0, row[3])
        self.entry_link.insert(0, row[4])
        self.entry_author.insert(0, row[5])
        self.entry_comments.insert(0, row[6])
        self.entry_risk.insert(0, row[7])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title("Поиск ")
        self.geometry("700x100+400+300")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Поиск записей")
        label_search.place(x=10, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=120, y=20, width=500)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=105, y=50)
        btn_search.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")


class Search_link(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search_link()
        self.view = app

    def init_search_link(self):
        self.title("Поиск по ссылке ")
        self.geometry("700x100+400+300")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Поиск записей по ссылке")
        label_search.place(x=10, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=170, y=20, width=500)

        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=105, y=50)
        btn_search.bind(
            "<Button-1>",
            lambda event: self.view.search_link_records(
                self.entry_search.get()
            ),
        )
        btn_search.bind("<Button-1>", lambda event: self.destroy(), add="+")


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("destructive_content.db")
        self.curs = self.conn.cursor()
        self.curs.execute(
            """CREATE TABLE IF NOT EXISTS destructive_content 
           (id integer primary key, 
           description text, 
           type text, 
           activity integer, 
           link text, 
           author text, 
           comments integer,
           risk real)"""
        )
        self.conn.commit()

    def insert_data(
        self, description, type, activity, link, author, comments, risk
    ):
        self.curs.execute(
            """ INSERT INTO destructive_content (description, 
           type, 
           activity, 
           link, 
           author, 
           comments, 
           risk)
           
           VALUES(?, ?, ?, ?, ?, ?, ?)""",
            (description, type, activity, link, author, comments, risk),
        )

        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("База данных о контентах с признаками деструктивности")
    root.geometry("1600x400+0+200")
    root.resizable(False, False)
    root.mainloop()
