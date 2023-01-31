from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.utils import platform

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

from database import Database

# Initialize db instance
db = Database()


class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        '''mark the task as complete or incomplete'''
        if check.active == True:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_task_as_complete(the_list_item.pk)  # here
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))  # Here

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)  # Here


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''


class MainApp(MDApp):
    task_list_dialog = None

    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.theme_font_styles = 'H6'

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Añadir coso",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def on_start(self):
        """Load the saved tasks and add them to the MDList widget when the application starts"""
        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()

            if uncomplete_tasks != []:
                for task in uncomplete_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text=task[1])
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text='[s]' + task[1] + '[/s]')
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task):
        '''Add task to the list of tasks'''

        # Add task to the db
        created_task = db.create_task(task.text)  # Here

        # return the created task details and create a list item
        self.root.ids['container'].add_widget(
            ListItemWithCheckbox(pk=created_task[0], text='[b]' + created_task[1] + '[/b]'))  # Here
        task.text = ''


if __name__ == '__main__':
    app = MainApp()
    app.run()