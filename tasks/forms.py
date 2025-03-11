from django import forms
from tasks.models import Task,TaskDetail

# Django Form
class TaskForm(forms.Form):
    title = forms.CharField(max_length=350, label="Task Title")
    description = forms.CharField(widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label="Assigned To")

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop('employees', [])
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]

class StyleFormMixin:
    default_classes = "border-2 border-gray-300 w-full rounded-lg shadow-sm hover:border-blue-500 p-2"
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput)):
                field.widget.attrs.update({'class': self.default_classes, "placeholder": f"Enter {field.label.lower()}"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': f"{self.default_classes} resize-none", "placeholder": f"Describe the {field.label.lower()}", "rows": 5})
                                           
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({'class': "border-2 border-gray-300  rounded-lg shadow-sm hover:border-blue-500 p-2"})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': "space-y-2"})
            
        

# Django Model Form
class TaskModelForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'assigned_to']
        widgets = {
            "due_date": forms.SelectDateWidget,
            "assigned_to": forms.CheckboxSelectMultiple
        }
        
        """ Manual Widget Styling """
        # widgets = {
        #     "title": forms.TextInput(attrs={'class': "border-2 border-gray-300 w-full rounded-lg shadow-sm hover:border-blue-500 p-2", 'name': "title", 'placeholder': "Enter Task Title"}),
        #     "description": forms.Textarea(attrs={'class': "border-2 border-gray-300 w-full rounded-lg shadow-sm hover:border-blue-500 p-2", 'name': "description", 'placeholder': "Describe the task", 'rows': 5}),
        #     "due_date": forms.SelectDateWidget(attrs={'class': "border-2 border-gray-300 rounded-lg shadow-sm hover:border-blue-500 p-2", 'name': "due_date"}),
            
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={'class': "space-y-2", 'name': "assigned_to"})
        # }
    
    """ Using Mixin for Widget Styling """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()


class TaskDetailModelForm(StyleFormMixin,forms.ModelForm):
    class Meta:
        model = TaskDetail
        fields = [ 'priority', 'notes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()