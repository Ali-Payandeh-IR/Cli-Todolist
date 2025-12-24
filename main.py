# Todo Manager Application
# A simple CLI todo app with Persian/English support

import json
import os
from datetime import datetime
import pytz
import threading
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from plyer import notification
from playsound import playsound

console = Console()
DATA_FILE = 'data.json'
tehran_tz = pytz.timezone('Asia/Tehran')

CATEGORIES = ['Work', 'Personal', 'Important', 'Other']
PRIORITIES = ['Low', 'Medium', 'High']

LANGUAGES = {
    'en': {
        'welcome_title': 'Todo Manager',
        'welcome_text': 'Manage your tasks efficiently with reminders, categories, and more.',
        'features': 'Features:',
        'feature_list': '• Add, edit, delete tasks\n• Set reminders with notifications\n• Categorize and prioritize\n• Search and filter\n• Statistics dashboard\n• Data backup',
        'menu_title': 'Main Menu',
        'menu_options': [
            '📋 Show All Tasks',
            '➕ Add New Task',
            '✅ Toggle Task Completion',
            '🗑️  Delete Task',
            '✏️  Edit Task',
            '⏰ Set Reminder/Timer',
            '📅 Today\'s Tasks',
            '🔍 Search Tasks',
            '🔽 Filter Tasks',
            '📊 Statistics',
            '💾 Backup Data',
            '🌐 Switch Language',
            '🚪 Exit'
        ],
        'choose_option': 'Choose an option',
        'todo_list_title': 'Todo List',
        'id': 'ID',
        'title': 'Title',
        'category': 'Category',
        'priority': 'Priority',
        'status': 'Status',
        'reminder': 'Reminder',
        'add_task_title': 'Add New Task',
        'task_title': 'Task Title',
        'description': 'Description',
        'task_added': 'Task added successfully!',
        'enter_id': 'Enter Task ID',
        'invalid_id': 'Invalid ID!',
        'task_completed': 'completed',
        'task_incomplete': 'incomplete',
        'status_changed': 'Task status changed!',
        'task_deleted': 'Task deleted successfully!',
        'edit_task_title': 'Edit Task',
        'new_title': 'New Title',
        'new_description': 'New Description',
        'new_category': 'New Category',
        'new_priority': 'New Priority',
        'task_updated': 'Task updated successfully!',
        'task_not_found': 'Task not found!',
        'set_reminder': 'Set Reminder',
        'reminder_datetime': 'Reminder Date & Time (YYYY-MM-DD HH:MM)',
        'reminder_set': 'Reminder set successfully!',
        'invalid_date': 'Invalid date format!',
        'search_query': 'Search Query',
        'filter_category': 'Category (leave empty for all)',
        'filter_priority': 'Priority (leave empty for all)',
        'filter_completed': 'Completed? (y/n/empty)',
        'stats_title': 'Statistics',
        'total_tasks': 'Total Tasks',
        'completed': 'Completed',
        'pending': 'Pending',
        'categories': 'Categories',
        'priorities': 'Priorities',
        'backup_created': 'Backup created successfully!',
        'goodbye': 'Goodbye!',
        'switch_lang': 'Switch Language',
        'choose_lang': 'Choose language (en/fa)',
        'lang_set': 'Language set to'
    },
    'fa': {
        'welcome_title': 'مدیریت کارها',
        'welcome_text': 'کارهای خود را به طور کارآمد با یادآورها، دسته‌بندی‌ها و موارد دیگر مدیریت کنید.',
        'features': 'ویژگی‌ها:',
        'feature_list': '• افزودن، ویرایش، حذف کارها\n• تنظیم یادآور با اعلان‌ها\n• دسته‌بندی و اولویت‌بندی\n• جستجو و فیلتر\n• داشبورد آمار\n• پشتیبان‌گیری داده‌ها',
        'menu_title': 'منوی اصلی',
        'menu_options': [
            '📋 نمایش همه کارها',
            '➕ افزودن کار جدید',
            '✅ تغییر وضعیت تکمیل',
            '🗑️  حذف کار',
            '✏️  ویرایش کار',
            '⏰ تنظیم یادآور/تایمر',
            '📅 کارهای امروز',
            '🔍 جستجوی کارها',
            '🔽 فیلتر کارها',
            '📊 آمار',
            '💾 پشتیبان‌گیری',
            '🌐 تغییر زبان',
            '🚪 خروج'
        ],
        'choose_option': 'انتخاب کنید',
        'todo_list_title': 'لیست کارها',
        'id': 'شماره',
        'title': 'عنوان',
        'category': 'دسته‌بندی',
        'priority': 'اولویت',
        'status': 'وضعیت',
        'reminder': 'یادآور',
        'add_task_title': 'افزودن کار جدید',
        'task_title': 'عنوان کار',
        'description': 'توضیحات',
        'task_added': 'کار اضافه شد!',
        'enter_id': 'شماره کار را وارد کنید',
        'invalid_id': 'شماره نامعتبر!',
        'task_completed': 'تکمیل شده',
        'task_incomplete': 'ناتکمیل',
        'status_changed': 'وضعیت تغییر کرد!',
        'task_deleted': 'کار حذف شد!',
        'edit_task_title': 'ویرایش کار',
        'new_title': 'عنوان جدید',
        'new_description': 'توضیحات جدید',
        'new_category': 'دسته‌بندی جدید',
        'new_priority': 'اولویت جدید',
        'task_updated': 'کار ویرایش شد!',
        'task_not_found': 'کار یافت نشد!',
        'set_reminder': 'تنظیم یادآور',
        'reminder_datetime': 'تاریخ و زمان یادآور (YYYY-MM-DD HH:MM)',
        'reminder_set': 'یادآور تنظیم شد!',
        'invalid_date': 'فرمت تاریخ نامعتبر!',
        'search_query': 'عبارت جستجو',
        'filter_category': 'دسته‌بندی (خالی برای همه)',
        'filter_priority': 'اولویت (خالی برای همه)',
        'filter_completed': 'تکمیل شده؟ (y/n/خالی)',
        'stats_title': 'آمار',
        'total_tasks': 'کل کارها',
        'completed': 'تکمیل شده',
        'pending': 'در انتظار',
        'categories': 'دسته‌بندی‌ها',
        'priorities': 'اولویت‌ها',
        'backup_created': 'پشتیبان گرفته شد!',
        'goodbye': 'خداحافظ!',
        'switch_lang': 'تغییر زبان',
        'choose_lang': 'زبان را انتخاب کنید (en/fa)',
        'lang_set': 'زبان تنظیم شد به'
    }
}

current_lang = 'en'

def _(key):
    return LANGUAGES[current_lang].get(key, key)

class Todo:
    def __init__(self, id, title, description, category, priority, completed=False, reminder=None):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority
        self.completed = completed
        self.reminder = reminder

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            todos = []
            for item in data.get('todos', []):
                reminder = None
                if item.get('reminder'):
                    reminder = datetime.fromisoformat(item['reminder']).replace(tzinfo=tehran_tz)
                todo = Todo(item['id'], item['title'], item['description'], item['category'], item['priority'], item['completed'], reminder)
                todos.append(todo)
            return todos
    return []

def save_todos(todos):
    data = {'todos': []}
    for todo in todos:
        item = {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'category': todo.category,
            'priority': todo.priority,
            'completed': todo.completed,
            'reminder': todo.reminder.isoformat() if todo.reminder else None
        }
        data['todos'].append(item)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def display_todos(todos, filter_func=None):
    table = Table(title=f"[bold blue]📋 { _('todo_list_title') }[/bold blue]", show_header=True, header_style="bold magenta", box=None)
    table.add_column(_('id'), style="cyan bold", no_wrap=True, justify="center")
    table.add_column(_('title'), style="white bold", max_width=30)
    table.add_column(_('category'), style="green", justify="center")
    table.add_column(_('priority'), style="yellow", justify="center")
    table.add_column(_('status'), style="red bold", justify="center")
    table.add_column(_('reminder'), style="blue", justify="center")
    for todo in todos:
        if filter_func and not filter_func(todo):
            continue
        status = "[green]✓[/green]" if todo.completed else "[red]✗[/red]"
        reminder_str = todo.reminder.strftime("%Y-%m-%d %H:%M") if todo.reminder else "-"
        table.add_row(str(todo.id), todo.title, todo.category, todo.priority, status, reminder_str)
    panel = Panel(table, title="[bold green]Tasks Overview[/bold green]", border_style="blue", padding=(1, 2))
    console.print(panel)

def add_todo(todos):
    console.print(f"[bold cyan]➕ { _('add_task_title') }[/bold cyan]")
    title = Prompt.ask(f"[yellow]{ _('task_title') }[/yellow]")
    description = Prompt.ask(f"[yellow]{ _('description') }[/yellow]")
    category = Prompt.ask(f"[green]{ _('category') }[/green]", choices=CATEGORIES)
    priority = Prompt.ask(f"[red]{ _('priority') }[/red]", choices=PRIORITIES)
    id = max([t.id for t in todos], default=0) + 1
    todo = Todo(id, title, description, category, priority)
    todos.append(todo)
    save_todos(todos)
    console.print(f"[green]✓ { _('task_added') }[/green]")

def mark_complete(todos):
    display_todos(todos)
    id_str = Prompt.ask(f"[cyan]{ _('enter_id') } to toggle completion[/cyan]")
    try:
        id = int(id_str)
    except ValueError:
        console.print(f"[red]✗ { _('invalid_id') }[/red]")
        return
    for todo in todos:
        if todo.id == id:
            todo.completed = not todo.completed
            save_todos(todos)
            status = _('task_completed') if todo.completed else _('task_incomplete')
            console.print(f"[green]✓ { _('status_changed') } {status}![/green]")
            return
    console.print(f"[red]✗ { _('task_not_found') }[/red]")

def delete_todo(todos):
    display_todos(todos)
    id_str = Prompt.ask(f"[cyan]{ _('enter_id') } to delete[/cyan]")
    try:
        id = int(id_str)
    except ValueError:
        console.print(f"[red]✗ { _('invalid_id') }[/red]")
        return
    for i, todo in enumerate(todos):
        if todo.id == id:
            todos.pop(i)
            save_todos(todos)
            console.print(f"[green]✓ { _('task_deleted') }[/green]")
            return
    console.print(f"[red]✗ { _('task_not_found') }[/red]")

def edit_todo(todos):
    display_todos(todos)
    id_str = Prompt.ask(f"[cyan]{ _('enter_id') } to edit[/cyan]")
    try:
        id = int(id_str)
    except ValueError:
        console.print(f"[red]✗ { _('invalid_id') }[/red]")
        return
    for todo in todos:
        if todo.id == id:
            console.print(f"[bold cyan]📝 { _('edit_task_title') }[/bold cyan]")
            todo.title = Prompt.ask(f"[yellow]{ _('new_title') }[/yellow]", default=todo.title)
            todo.description = Prompt.ask(f"[yellow]{ _('new_description') }[/yellow]", default=todo.description)
            todo.category = Prompt.ask(f"[green]{ _('new_category') }[/green]", choices=CATEGORIES, default=todo.category)
            todo.priority = Prompt.ask(f"[red]{ _('new_priority') }[/red]", choices=PRIORITIES, default=todo.priority)
            save_todos(todos)
            console.print(f"[green]✓ { _('task_updated') }[/green]")
            return
    console.print(f"[red]✗ { _('task_not_found') }[/red]")

def set_reminder(todos):
    display_todos(todos)
    id_str = Prompt.ask(f"[cyan]{ _('enter_id') } to set reminder[/cyan]")
    try:
        id = int(id_str)
    except ValueError:
        console.print(f"[red]✗ { _('invalid_id') }[/red]")
        return
    for todo in todos:
        if todo.id == id:
            date_str = Prompt.ask(f"[blue]{ _('reminder_datetime') }[/blue]")
            try:
                reminder = datetime.strptime(date_str, "%Y-%m-%d %H:%M").replace(tzinfo=tehran_tz)
                todo.reminder = reminder
                save_todos(todos)
                console.print(f"[green]✓ { _('reminder_set') }[/green]")
                # start timer thread
                threading.Thread(target=reminder_thread, args=(todo,), daemon=True).start()
            except ValueError:
                console.print(f"[red]✗ { _('invalid_date') }[/red]")
            return
    console.print(f"[red]✗ { _('task_not_found') }[/red]")

def reminder_thread(todo):
    now = datetime.now(tehran_tz)
    if todo.reminder > now:
        sleep_time = (todo.reminder - now).total_seconds()
        time.sleep(sleep_time)
        # notify
        notification.notify(
            title="Task Reminder",
            message=f"Reminder: {todo.title}",
            app_name="Todo App"
        )
        # sound
        try:
            playsound('notification.mp3')  # assume a sound file exists
        except:
            pass

def search_todos(todos):
    query = Prompt.ask(f"[magenta]🔍 { _('search_query') }[/magenta]")
    filtered = [t for t in todos if query.lower() in t.title.lower() or query.lower() in t.description.lower()]
    display_todos(filtered)

def filter_todos(todos):
    category = Prompt.ask(f"[green]{ _('filter_category') }[/green]", choices=CATEGORIES + [""], default="")
    priority = Prompt.ask(f"[red]{ _('filter_priority') }[/red]", choices=PRIORITIES + [""], default="")
    completed = Prompt.ask(f"[yellow]{ _('filter_completed') }[/yellow]", choices=["y","n",""], default="")
    def filter_func(todo):
        if category and todo.category != category:
            return False
        if priority and todo.priority != priority:
            return False
        if completed == "y" and not todo.completed:
            return False
        if completed == "n" and todo.completed:
            return False
        return True
    display_todos(todos, filter_func)

def show_stats(todos):
    total = len(todos)
    completed = sum(1 for t in todos if t.completed)
    pending = total - completed
    categories_count = {cat: sum(1 for t in todos if t.category == cat) for cat in CATEGORIES}
    priorities_count = {pri: sum(1 for t in todos if t.priority == pri) for pri in PRIORITIES}
    stats_panel = Panel(
        f"[bold cyan]📊 { _('stats_title') }[/bold cyan]\n\n"
        f"{ _('total_tasks') }: [yellow]{total}[/yellow]\n"
        f"{ _('completed') }: [green]{completed}[/green]\n"
        f"{ _('pending') }: [red]{pending}[/red]\n\n"
        f"[bold]{ _('categories') }:[/bold]\n" +
        "\n".join(f"  {cat}: {count}" for cat, count in categories_count.items()) + "\n\n"
        f"[bold]{ _('priorities') }:[/bold]\n" +
        "\n".join(f"  {pri}: {count}" for pri, count in priorities_count.items()),
        title="[bold green]Dashboard[/bold green]", border_style="green", padding=(1, 2)
    )
    console.print(stats_panel)

def backup_todos(todos):
    import shutil
    shutil.copy(DATA_FILE, f"{DATA_FILE}.backup")
    console.print(f"[green]✓ { _('backup_created') }[/green]")

def switch_language():
    global current_lang
    lang = Prompt.ask(f"[blue]{ _('choose_lang') }[/blue]", choices=["en", "fa"])
    current_lang = lang
    console.print(f"[green]✓ { _('lang_set') } {lang.upper()}![/green]")

def main_menu(todos):
    while True:
        menu_options = _('menu_options')
        menu_panel = Panel(
            f"[bold cyan]🚀 { _('menu_title') }[/bold cyan]\n\n" +
            "\n".join(f"[{i+1}] {opt}" for i, opt in enumerate(menu_options)),
            title="[bold green]Todo Manager[/bold green]", border_style="blue", padding=(1, 2)
        )
        console.print(menu_panel)
        choices = [str(i+1) for i in range(len(menu_options))]
        choice = Prompt.ask(f"[yellow]{ _('choose_option') }[/yellow]", choices=choices)
        if choice == "1":
            display_todos(todos)
        elif choice == "2":
            add_todo(todos)
        elif choice == "3":
            mark_complete(todos)
        elif choice == "4":
            delete_todo(todos)
        elif choice == "5":
            edit_todo(todos)
        elif choice == "6":
            set_reminder(todos)
        elif choice == "7":
            # today's tasks
            today = datetime.now(tehran_tz).date()
            display_todos(todos, lambda t: t.reminder and t.reminder.date() == today)
        elif choice == "8":
            search_todos(todos)
        elif choice == "9":
            filter_todos(todos)
        elif choice == "10":
            show_stats(todos)
        elif choice == "11":
            backup_todos(todos)
        elif choice == "12":
            switch_language()
        elif choice == "13":
            console.print(f"[bold green]👋 { _('goodbye') }![/bold green]")
            break

if __name__ == "__main__":
    welcome_panel = Panel(
        f"[bold cyan]🎯 { _('welcome_text') }[/bold cyan]\n\n"
        f"[dim]{ _('features') }[/dim]\n"
        f"{ _('feature_list') }",
        title=f"[bold magenta]🚀 { _('welcome_title') }[/bold magenta]", border_style="magenta", padding=(1, 2)
    )
    console.print(welcome_panel)
    todos = load_todos()
    # start reminder threads for existing
    for todo in todos:
        if todo.reminder and todo.reminder > datetime.now(tehran_tz):
            threading.Thread(target=reminder_thread, args=(todo,), daemon=True).start()
    main_menu(todos)