import tkinter as tk
from tkinter import messagebox
import requests
import tkinter.ttk as ttk


class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("个人财务系统")
        self.geometry("800x650")

        self.current_frame = None  # 用来保存当前显示的Frame
        self.cookies = {}  # 用于存储登录时的 cookies
        self.logged_in_username = ""  # 存储登录后的用户名
        self.show_home_page()  # 初始页面显示主页

    def switch_frame(self, frame_class, *args, **kwargs):
        """切换页面"""
        new_frame = frame_class(self, *args, **kwargs)
        if self.current_frame:
            self.current_frame.destroy()  # 销毁当前页面
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def show_home_page(self):
        """主页"""
        self.switch_frame(HomePage)

    def show_function_menu(self):
        """功能菜单页面"""
        self.switch_frame(UserMenuPage)


class AddAccountPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="新增账户", font=("Arial", 24))
        title_label.pack(pady=50)

        account_name_label = tk.Label(self, text="账户名称", font=("Arial", 12))
        account_name_label.pack(pady=5)
        self.account_name_entry = tk.Entry(self, font=("Arial", 12))
        self.account_name_entry.pack(pady=5)

        account_type_label = tk.Label(self, text="账户类型", font=("Arial", 12))
        account_type_label.pack(pady=5)
        self.account_type_entry = tk.Entry(self, font=("Arial", 12))
        self.account_type_entry.pack(pady=5)

        submit_button = tk.Button(self, text="提交", font=("Arial", 14), command=self.submit_account)
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def submit_account(self):
        account_name = self.account_name_entry.get()
        account_type = self.account_type_entry.get()

        if not account_name or not account_type:
            messagebox.showerror("错误", "所有字段都是必填的")
            return

        payload = {
            "accountname": account_name,
            "accounttype": account_type
        }

        try:
            response = requests.post("http://38.147.186.51:8000/account/add_account/", json=payload,
                                     cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                messagebox.showinfo("账户创建成功", response_data["message"])
                self.master.switch_frame(AccountPage)
            else:
                messagebox.showerror("账户创建失败", response_data["message"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def go_back(self):
        self.master.switch_frame(AccountPage)


class HomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="个人财务系统", font=("Arial", 24))
        title_label.pack(pady=50)

        login_button = tk.Button(self, text="登录", font=("Arial", 14), command=self.show_login_page)
        login_button.pack(pady=10)

        register_button = tk.Button(self, text="注册", font=("Arial", 14), command=self.show_register_page)
        register_button.pack(pady=10)

    def show_login_page(self):
        self.master.switch_frame(LoginPage)

    def show_register_page(self):
        self.master.switch_frame(RegisterPage)


class EditAccountPage(tk.Frame):
    def __init__(self, master, account_id):
        super().__init__(master)
        self.master = master
        self.account_id = account_id
        self.account_details = {}
        self.create_widgets()
        self.fetch_account_details()

    def create_widgets(self):
        title_label = tk.Label(self, text="修改账户", font=("Arial", 24))
        title_label.pack(pady=50)

        account_name_label = tk.Label(self, text="账户名称", font=("Arial", 12))
        account_name_label.pack(pady=5)
        self.account_name_entry = tk.Entry(self, font=("Arial", 12))
        self.account_name_entry.pack(pady=5)

        account_type_label = tk.Label(self, text="账户类型", font=("Arial", 12))
        account_type_label.pack(pady=5)
        self.account_type_entry = tk.Entry(self, font=("Arial", 12))
        self.account_type_entry.pack(pady=5)

        submit_button = tk.Button(self, text="提交", font=("Arial", 14), command=self.submit_update)
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def fetch_account_details(self):
        try:
            url = "http://38.147.186.51:8000/account/get_account_details/"
            payload = {"account_id": self.account_id}

            response = requests.post(url, json=payload, cookies=self.master.cookies)

            response_data = response.json()

            if response_data["code"] == 200:
                self.account_details = response_data["data"]
                self.populate_fields()
            else:
                messagebox.showerror("获取账户信息失败", response_data["message"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def populate_fields(self):
        self.account_name_entry.delete(0, tk.END)
        self.account_name_entry.insert(0, self.account_details.get("accountname", ""))
        self.account_type_entry.delete(0, tk.END)
        self.account_type_entry.insert(0, self.account_details.get("accounttype", ""))

    def submit_update(self):
        account_name = self.account_name_entry.get()
        account_type = self.account_type_entry.get()

        if not account_name or not account_type:
            messagebox.showerror("错误", "所有字段都是必填的")
            return

        payload = {
            "account_id": self.account_id,
            "accountname": account_name,
            "accounttype": account_type
        }

        try:
            response = requests.post("http://38.147.186.51:8000/account/update_account/", json=payload,
                                     cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                messagebox.showinfo("账户信息更新成功", response_data["message"])
                self.master.switch_frame(AccountPage)
            else:
                messagebox.showerror("账户信息更新失败", response_data["message"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def go_back(self):
        self.master.switch_frame(AccountPage)


class AccountPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.accounts = []
        self.create_widgets()
        self.fetch_accounts()

    def create_widgets(self):
        title_label = tk.Label(self, text="我的账户", font=("Arial", 24))
        title_label.pack(pady=50)
        edit_account_button = tk.Button(self, text="修改账户", command=self.edit_selected_account)
        edit_account_button.pack(pady=10)
        # 创建 Treeview 表格
        columns = ("accountname", "accounttype", "accountbalance")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        self.tree.heading('accountname', text='账户名称')
        self.tree.heading('accounttype', text='账户类型')
        self.tree.heading('accountbalance', text='账户余额')

        self.tree.column('accountname', width=150)
        self.tree.column('accounttype', width=100)
        self.tree.column('accountbalance', width=100)

        self.tree.bind('<ButtonRelease-1>', self.select_item)  # 绑定点击事件

        self.tree.pack(pady=20)

        add_account_button = tk.Button(self, text="新增账户", command=lambda: self.master.switch_frame(AddAccountPage))
        add_account_button.pack(pady=10)

        delete_account_button = tk.Button(self, text="删除账户", command=self.delete_selected_account)
        delete_account_button.pack(pady=10)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def edit_selected_account(self):
        if hasattr(self, 'selected_account_id') and self.selected_account_id is not None:
            self.master.switch_frame(EditAccountPage, self.selected_account_id)
        else:
            messagebox.showwarning("未选择账户", "请选择一个账户进行修改")

    def fetch_accounts(self):
        try:
            response = requests.get("http://38.147.186.51:8000/account/get_user_accounts/", cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                self.accounts = response_data["data"]
                self.populate_tree()
            else:
                messagebox.showerror("获取账户信息失败", response_data["message"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for account in self.accounts:
            self.tree.insert("", "end",
                             values=(account['accountname'], account['accounttype'], account['accountbalance']))

    def go_back(self):
        self.master.switch_frame(UserMenuPage)

    def select_item(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], 'values')
            self.selected_account_id = next(
                (acc['accountid'] for acc in self.accounts if acc['accountname'] == item_values[0]), None)

    def delete_selected_account(self):
        if hasattr(self, 'selected_account_id') and self.selected_account_id is not None:
            payload = {
                "account_id": self.selected_account_id
            }

            try:
                response = requests.post("http://38.147.186.51:8000/account/delete_account/", json=payload,
                                         cookies=self.master.cookies)
                response_data = response.json()

                if response_data["code"] == 200:
                    messagebox.showinfo("账户删除成功", response_data["message"])
                    self.fetch_accounts()  # 刷新账户列表
                else:
                    messagebox.showerror("账户删除失败", response_data["message"])

            except requests.exceptions.RequestException as e:
                messagebox.showerror("请求失败", f"无法连接到服务器：{e}")
        else:
            messagebox.showwarning("未选择账户", "请选择一个账户进行删除")


class AddBudgetPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="新增预算", font=("Arial", 24))
        title_label.pack(pady=50)

        account_id_label = tk.Label(self, text="账户ID", font=("Arial", 12))
        account_id_label.pack(pady=5)
        self.account_id_entry = tk.Entry(self, font=("Arial", 12))
        self.account_id_entry.pack(pady=5)

        budget_name_label = tk.Label(self, text="预算名称", font=("Arial", 12))
        budget_name_label.pack(pady=5)
        self.budget_name_entry = tk.Entry(self, font=("Arial", 12))
        self.budget_name_entry.pack(pady=5)

        budget_type_label = tk.Label(self, text="预算类型", font=("Arial", 12))
        budget_type_label.pack(pady=5)
        self.budget_type_entry = tk.Entry(self, font=("Arial", 12))
        self.budget_type_entry.pack(pady=5)

        budget_balance_label = tk.Label(self, text="预算余额", font=("Arial", 12))
        budget_balance_label.pack(pady=5)
        self.budget_balance_entry = tk.Entry(self, font=("Arial", 12))
        self.budget_balance_entry.pack(pady=5)

        submit_button = tk.Button(self, text="提交", font=("Arial", 14), command=self.submit_budget)
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def submit_budget(self):
        account_id = self.account_id_entry.get()
        budget_name = self.budget_name_entry.get()
        budget_type = self.budget_type_entry.get()
        budget_balance = self.budget_balance_entry.get()

        if not account_id or not budget_name or not budget_type or not budget_balance:
            messagebox.showerror("错误", "所有字段都是必填的")
            return

        payload = {
            "account_id": int(account_id),
            "budgetname": budget_name,
            "budgettype": budget_type,
            "budgetbalance": float(budget_balance)
        }

        try:
            response = requests.post("http://38.147.186.51:8000/budget/add_budget/", json=payload,
                                     cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                messagebox.showinfo("预算创建成功", response_data["message"])
                self.master.switch_frame(BudgetPage)
            else:
                messagebox.showerror("预算创建失败", response_data["message"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def go_back(self):
        self.master.switch_frame(BudgetPage)


class BudgetPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.budgets = []
        self.selected_budget_id = None  # 新增属性
        self.create_widgets()
        self.fetch_budgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="我的预算", font=("Arial", 24))
        title_label.pack(pady=50)

        # 新增预算按钮
        add_budget_button = tk.Button(self, text="新增预算", command=self.show_add_budget_page)
        add_budget_button.pack(pady=10)

        # 编辑预算按钮
        edit_budget_button = tk.Button(self, text="编辑预算", command=self.edit_selected_budget)
        edit_budget_button.pack(pady=10)

        # 删除预算按钮
        delete_budget_button = tk.Button(self, text="删除预算", command=self.delete_selected_budget)
        delete_budget_button.pack(pady=10)

        # 创建 Treeview 表格
        columns = ("budgetid", "budgetname", "budgettype", "budgetbalance", "accountname", "accounttype")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        self.tree.heading('budgetid', text='预算id')
        self.tree.heading('budgetname', text='预算名称')
        self.tree.heading('budgettype', text='预算类型')
        self.tree.heading('budgetbalance', text='预算余额')
        self.tree.heading('accountname', text='账户名称')
        self.tree.heading('accounttype', text='账户类型')

        self.tree.column('budgetid', width=150)
        self.tree.column('budgetname', width=150)
        self.tree.column('budgettype', width=100)
        self.tree.column('budgetbalance', width=100)
        self.tree.column('accountname', width=150)
        self.tree.column('accounttype', width=100)

        self.tree.bind('<ButtonRelease-1>', self.select_item)  # 绑定点击事件

        self.tree.pack(pady=20)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def show_add_budget_page(self):
        self.master.switch_frame(AddBudgetPage)

    def edit_selected_budget(self):
        if self.selected_budget_id is not None:
            self.master.switch_frame(EditBudgetPage, self.selected_budget_id)
        else:
            messagebox.showwarning("未选择预算", "请选择一个预算进行编辑")

    def delete_selected_budget(self):
        if self.selected_budget_id is not None:
            payload = {
                "budget_id": self.selected_budget_id
            }

            try:
                response = requests.post("http://38.147.186.51:8000/budget/delete_budget/", json=payload,
                                         cookies=self.master.cookies)
                response_data = response.json()

                if response_data["code"] == 200:
                    messagebox.showinfo("预算删除成功", response_data["message"])
                    self.fetch_budgets()  # 刷新预算列表
                else:
                    messagebox.showerror("预算删除失败", response_data["message"])

            except requests.exceptions.RequestException as e:
                messagebox.showerror("请求失败", f"无法连接到服务器：{e}")
        else:
            messagebox.showwarning("未选择预算", "请选择一个预算进行删除")

    def fetch_budgets(self):
        try:
            response = requests.get("http://38.147.186.51:8000/budget/get_user_budgets/", cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                self.budgets = response_data["data"]
                self.populate_tree()
            else:
                messagebox.showerror("获取预算信息失败", response_data["message"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for budget in self.budgets:
            self.tree.insert("", "end",
                             values=(
                                 budget['budgetid'],
                                 budget['budgetname'],
                                 budget['budgettype'],
                                 budget['budgetbalance'],
                                 budget['accountname'],
                                 budget['accounttype']
                             ))

    def go_back(self):
        self.master.switch_frame(UserMenuPage)

    def select_item(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], 'values')
            self.selected_budget_id = int(item_values[0])


class RecordPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.trades = []
        self.create_widgets()
        self.fetch_trades()

    def create_widgets(self):
        title_label = tk.Label(self, text="收支记录", font=("Arial", 24))
        title_label.pack(pady=50)

        # 新增收支记录按钮
        add_trade_button = tk.Button(self, text="新增收支记录", command=self.show_add_trade_page)
        add_trade_button.pack(pady=10)

        # 创建 Treeview 表格
        columns = ("id", "account_name", "budget_name", "tradetype", "tradebalance", "traderemark")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=10)
        self.tree.heading('id', text='交易ID')
        self.tree.heading('account_name', text='账户名称')
        self.tree.heading('budget_name', text='预算名称')
        self.tree.heading('tradetype', text='交易类型')
        self.tree.heading('tradebalance', text='交易金额')
        self.tree.heading('traderemark', text='交易备注')

        self.tree.column('id', width=100)
        self.tree.column('account_name', width=150)
        self.tree.column('budget_name', width=150)
        self.tree.column('tradetype', width=100)
        self.tree.column('tradebalance', width=100)
        self.tree.column('traderemark', width=200)

        self.tree.pack(pady=20)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def show_add_trade_page(self):
        self.master.switch_frame(AddTradePage)
    def fetch_trades(self):
        try:
            response = requests.get("http://38.147.186.51:8000/trade/get_trades/", cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                self.trades = response_data["data"]
                self.populate_tree()
            else:
                messagebox.showerror("获取交易记录失败", response_data["message"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for trade in self.trades:
            self.tree.insert("", "end",
                             values=(
                                 trade['id'],
                                 trade['account_name'],
                                 trade['budget_name'] if trade['budget_name'] else "",
                                 trade['tradetype'],
                                 trade['tradebalance'],
                                 trade['traderemark']
                             ))

    def go_back(self):
        self.master.switch_frame(UserMenuPage)


class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

        title_label = tk.Label(self, text="注册", font=("Arial", 20))
        title_label.pack(pady=20)

        username_label = tk.Label(self, text="用户名", font=("Arial", 12))
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self, text="密码", font=("Arial", 12))
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        confirm_password_label = tk.Label(self, text="确认密码", font=("Arial", 12))
        confirm_password_label.pack(pady=5)
        self.confirm_password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.confirm_password_entry.pack(pady=5)

        email_label = tk.Label(self, text="邮箱", font=("Arial", 12))
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        register_button = tk.Button(self, text="完成注册", font=("Arial", 14), command=self.register)
        register_button.pack(pady=20)

    def go_back(self):
        self.master.switch_frame(HomePage)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        email = self.email_entry.get()

        # 验证输入
        if not username or not password or not confirm_password or not email:
            messagebox.showerror("错误", "所有字段都是必填的")
        elif password != confirm_password:
            messagebox.showerror("错误", "密码和确认密码不一致")
        else:
            # 准备请求体数据
            payload = {
                "username": username,
                "password": password,
                "email": email
            }
            # 发送 POST 请求到后端
            try:
                response = requests.post("http://38.147.186.51:8000/userpro/register/", json=payload)
                response_data = response.json()

                # 处理响应
                if response_data["code"] == 200:
                    messagebox.showinfo("注册成功", response_data["message"])
                    self.master.switch_frame(HomePage)  # 注册成功后跳转到主页
                else:
                    messagebox.showerror("注册失败", response_data["message"])

            except requests.exceptions.RequestException as e:
                messagebox.showerror("请求失败", f"无法连接到服务器：{e}")


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

        title_label = tk.Label(self, text="登录", font=("Arial", 20))
        title_label.pack(pady=20)

        username_label = tk.Label(self, text="用户名", font=("Arial", 12))
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self, text="密码", font=("Arial", 12))
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="登录", font=("Arial", 14), command=self.login)
        login_button.pack(pady=20)

    def go_back(self):
        self.master.switch_frame(HomePage)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码")
            return

        payload = {
            "username": username,
            "password": password
        }

        # 登录请求
        try:
            response = requests.post("http://38.147.186.51:8000/userpro/login/", json=payload)
            response_data = response.json()

            # 判断响应的状态码
            if response_data["code"] == 200:
                # 保存cookies
                self.master.cookies = response.cookies
                messagebox.showinfo("登录成功", response_data["message"])

                # 获取用户名并存储
                self.master.logged_in_username = response_data["data"]["username"]

                # 跳转到用户菜单页面
                self.master.switch_frame(UserMenuPage)
            else:
                messagebox.showerror("登录失败", response_data["message"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")


class EditBudgetPage(tk.Frame):
    def __init__(self, master, budget_id):
        super().__init__(master)
        self.master = master
        self.budget_id = budget_id
        self.budget_details = {}
        self.create_widgets()
        self.fetch_budget_details()

    def create_widgets(self):
        title_label = tk.Label(self, text="编辑预算", font=("Arial", 24))
        title_label.pack(pady=50)

        budget_name_label = tk.Label(self, text="预算名称", font=("Arial", 12))
        budget_name_label.pack(pady=5)
        self.budget_name_entry = tk.Entry(self, font=("Arial", 12))
        self.budget_name_entry.pack(pady=5)

        budget_type_label = tk.Label(self, text="预算类型", font=("Arial", 12))
        budget_type_label.pack(pady=5)
        self.budget_type_entry = tk.Entry(self, font=("Arial", 12))
        self.budget_type_entry.pack(pady=5)

        budget_balance_label = tk.Label(self, text="预算余额", font=("Arial", 12))
        budget_balance_label.pack(pady=5)
        self.budget_balance_entry = tk.Entry(self, font=("Arial", 12))
        self.budget_balance_entry.pack(pady=5)

        submit_button = tk.Button(self, text="提交", font=("Arial", 14), command=self.submit_update)
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def fetch_budget_details(self):
        try:
            url = "http://38.147.186.51:8000/budget/get_budget_detail/"
            payload = {"budget_id": self.budget_id}

            response = requests.post(url, json=payload, cookies=self.master.cookies)

            response_data = response.json()

            if response_data["code"] == 200:
                self.budget_details = response_data["data"]
                self.populate_fields()
            else:
                messagebox.showerror("获取预算信息失败", response_data["message"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def populate_fields(self):
        self.budget_name_entry.delete(0, tk.END)
        self.budget_name_entry.insert(0, self.budget_details.get("budgetname", ""))
        self.budget_type_entry.delete(0, tk.END)
        self.budget_type_entry.insert(0, self.budget_details.get("budgettype", ""))
        self.budget_balance_entry.delete(0, tk.END)
        self.budget_balance_entry.insert(0, str(self.budget_details.get("budgetbalance", "")))

    def submit_update(self):
        budget_name = self.budget_name_entry.get()
        budget_type = self.budget_type_entry.get()
        budget_balance = self.budget_balance_entry.get()

        if not budget_name or not budget_type or not budget_balance:
            messagebox.showerror("错误", "所有字段都是必填的")
            return

        payload = {
            "budget_id": self.budget_id,
            "budgetname": budget_name,
            "budgettype": budget_type,
            "budgetbalance": float(budget_balance)
        }

        try:
            response = requests.post("http://38.147.186.51:8000/budget/update_budget/", json=payload,
                                     cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                messagebox.showinfo("预算信息更新成功", response_data["message"])
                self.master.switch_frame(BudgetPage)
            else:
                messagebox.showerror("预算信息更新失败", response_data["message"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def go_back(self):
        self.master.switch_frame(BudgetPage)


class UserMenuPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # 显示用户名和下拉菜单按钮
        user_button = tk.Menubutton(self, text=f"{self.master.logged_in_username}", relief=tk.RAISED)
        user_button.menu = tk.Menu(user_button, tearoff=0)
        user_button["menu"] = user_button.menu

        user_button.menu.add_command(label="个人信息", command=self.show_profile_page)
        user_button.menu.add_command(label="退出登录", command=self.logout)
        user_button.pack(anchor="ne", padx=10, pady=10)

        title_label = tk.Label(self, text="功能菜单", font=("Arial", 24))
        title_label.pack(pady=50)

        # 添加三个功能按钮
        account_button = tk.Button(self, text="我的账户", font=("Arial", 14), command=self.show_account_page)
        account_button.pack(pady=10)

        budget_button = tk.Button(self, text="我的预算", font=("Arial", 14), command=self.show_budget_page)
        budget_button.pack(pady=10)

        record_button = tk.Button(self, text="收支记录", font=("Arial", 14), command=self.show_record_page)
        record_button.pack(pady=10)

    def logout(self):
        try:
            response = requests.get("http://38.147.186.51:8000/userpro/logout/", cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                messagebox.showinfo("退出登录", "您已成功退出登录")
                self.master.cookies = {}  # 清除 cookies
                self.master.logged_in_username = ""  # 清除用户名
                self.master.switch_frame(HomePage)  # 返回主页
            else:
                messagebox.showerror("退出失败", response_data["message"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def show_account_page(self):
        self.master.switch_frame(AccountPage)

    def show_budget_page(self):
        self.master.switch_frame(BudgetPage)

    def show_record_page(self):
        self.master.switch_frame(RecordPage)

    def show_profile_page(self):
        self.master.switch_frame(ProfilePage)


class ProfilePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.user_info = {}
        self.create_widgets()
        self.fetch_user_info()

    def create_widgets(self):
        title_label = tk.Label(self, text="个人信息", font=("Arial", 24))
        title_label.pack(pady=20)

        # 创建 Treeview 表格
        columns = ("key", "value")
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=5)
        self.tree.heading('key', text='Key')
        self.tree.heading('value', text='Value')

        self.tree.column('key', width=100)
        self.tree.column('value', width=200)

        self.tree.pack(pady=20)

        # 创建表单控件
        form_frame = tk.Frame(self)
        form_frame.pack(pady=20)

        labels = ["Nickname", "Birthday", "Gender", "Email"]
        entries = []
        for i, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, font=("Arial", 12))
            label.grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            entry = tk.Entry(form_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        self.nickname_entry, self.birthday_entry, self.gender_entry, self.email_entry = entries

        update_button = tk.Button(self, text="更新信息", command=self.update_profile)
        update_button.pack(pady=10)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def fetch_user_info(self):
        try:
            response = requests.get("http://38.147.186.51:8000/userpro/get_user_info/", cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                self.user_info = response_data["data"]
                self.populate_tree_and_entries()
            else:
                messagebox.showerror("获取信息失败", response_data["message"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def populate_tree_and_entries(self):
        self.tree.delete(*self.tree.get_children())
        for key, value in self.user_info.items():
            self.tree.insert("", "end", values=(key, str(value)))

        self.nickname_entry.delete(0, tk.END)
        self.birthday_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

        self.nickname_entry.insert(0, self.user_info.get("nickname", ""))
        self.birthday_entry.insert(0, self.user_info.get("birthday", ""))
        self.gender_entry.insert(0, self.user_info.get("gender", ""))
        self.email_entry.insert(0, self.user_info.get("email", ""))

    def update_profile(self):
        nickname = self.nickname_entry.get()
        birthday = self.birthday_entry.get()
        gender = self.gender_entry.get()
        email = self.email_entry.get()

        # 验证输入
        if not nickname or not birthday or not gender or not email:
            messagebox.showerror("错误", "所有字段都是必填的")
            return

        payload = {
            "nickname": nickname,
            "birthday": birthday,
            "gender": gender,
            "email": email
        }

        try:
            response = requests.post("http://38.147.186.51:8000/userpro/update_profile/", json=payload,
                                     cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                messagebox.showinfo("更新成功", response_data["message"])
                self.user_info = response_data["data"]
                self.populate_tree_and_entries()
            else:
                messagebox.showerror("更新失败", response_data["message"])
        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def go_back(self):
        self.master.switch_frame(UserMenuPage)


class AddTradePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="新增收支记录", font=("Arial", 24))
        title_label.pack(pady=50)

        account_id_label = tk.Label(self, text="账户ID", font=("Arial", 12))
        account_id_label.pack(pady=5)
        self.account_id_entry = tk.Entry(self, font=("Arial", 12))
        self.account_id_entry.pack(pady=5)

        budget_id_label = tk.Label(self, text="预算ID", font=("Arial", 12))
        budget_id_label.pack(pady=5)
        self.budget_id_entry = tk.Entry(self, font=("Arial", 12))
        self.budget_id_entry.pack(pady=5)

        traderemark_label = tk.Label(self, text="交易备注", font=("Arial", 12))
        traderemark_label.pack(pady=5)
        self.traderemark_entry = tk.Entry(self, font=("Arial", 12))
        self.traderemark_entry.pack(pady=5)

        tradebalance_label = tk.Label(self, text="交易金额", font=("Arial", 12))
        tradebalance_label.pack(pady=5)
        self.tradebalance_entry = tk.Entry(self, font=("Arial", 12))
        self.tradebalance_entry.pack(pady=5)

        tradetype_label = tk.Label(self, text="交易类型", font=("Arial", 12))
        tradetype_label.pack(pady=5)
        self.tradetype_entry = tk.Entry(self, font=("Arial", 12))
        self.tradetype_entry.pack(pady=5)

        submit_button = tk.Button(self, text="提交", font=("Arial", 14), command=self.submit_trade)
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="返回", command=self.go_back)
        back_button.pack(anchor="nw", padx=10, pady=10)

    def submit_trade(self):
        account_id = self.account_id_entry.get()
        budget_id = self.budget_id_entry.get()
        traderemark = self.traderemark_entry.get()
        tradebalance = self.tradebalance_entry.get()
        tradetype = self.tradetype_entry.get()

        if not account_id or not budget_id or not traderemark or not tradebalance or not tradetype:
            messagebox.showerror("错误", "所有字段都是必填的")
            return

        payload = {
            "account_id": int(account_id),
            "budget_id": int(budget_id),
            "traderemark": traderemark,
            "tradebalance": float(tradebalance),
            "tradetype": tradetype
        }

        try:
            response = requests.post("http://38.147.186.51:8000/trade/add_trade/", json=payload,
                                     cookies=self.master.cookies)
            response_data = response.json()

            if response_data["code"] == 200:
                messagebox.showinfo("交易记录创建成功", response_data["message"])
                self.master.switch_frame(RecordPage)
            else:
                messagebox.showerror("交易记录创建失败", response_data["message"])

        except requests.exceptions.RequestException as e:
            messagebox.showerror("请求失败", f"无法连接到服务器：{e}")

    def go_back(self):
        self.master.switch_frame(RecordPage)


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
