from django import forms
from django.forms import ModelForm
from .models import Computer, Processor, RAM, Disk


# class FilterForm(forms.Form):
# 	uniques = lambda l:list(set(l))
# 	choices = {}
# 	processors = Processor.objects.all()
# 	choices['cpuModels'] = [('', 'Any')]+uniques([(cpu.model, cpu.model) for cpu in processors])
# 	choices['cpuSpeeds'] = [('', 'Any')]+uniques([(cpu.speed, cpu.speed) for cpu in processors])
# 	rams = RAM.objects.all()
# 	choices['ramModels'] = [('', 'Any')]+uniques([(ram.model, ram.model) for ram in rams])
# 	choices['ramSpeeds'] = [('', 'Any')]+uniques([(ram.speed, ram.speed) for ram in rams])
# 	choices['disks'] = [('', 'Any')]+uniques([(disk, disk) for disk in Disk.objects.all()])

# 	processorModel = forms.ChoiceField(label = 'CPU Model', choices = choices['cpuModels'], required = False)
# 	processorSpeed = forms.ChoiceField(label = 'CPU Speed', choices = choices['cpuSpeeds'], required = False)
# 	ramModel = forms.ChoiceField(label = 'RAM Model', choices = choices['ramModels'], required = False)
# 	ramSpeed = forms.ChoiceField(label = 'RAM Speed', choices = choices['ramSpeeds'], required = False)
# 	diskType = forms.ChoiceField(label = 'Disk', choices = choices['disks'], required = False)


class ComputerForm(ModelForm):
	prefix = 'pc'
	class Meta:
		model = Computer
		fields = [
		'processor',
		'ram',
		'disk',
		'photo'
		]

class ProcessorForm(ModelForm):
	prefix = 'cpu'
	class Meta:
		model = Processor
		fields = [
		'model',
		'speed',
		]
	def __init__(self, *args, **kwargs):
		super(ProcessorForm, self).__init__(*args, **kwargs)
		self.fields['model'].required = False
		self.fields['model'].label = 'CPU Model'

		self.fields['speed'].required = False
		self.fields['speed'].label = 'CPU Speed'

	def clean(self):
		cleaned_data = super().clean()
		model = cleaned_data.get('model')
		speed = cleaned_data.get('speed')
		notexist = 'No such entries!'
		if not Processor.objects.filter(model__icontains = model):
			self.add_error('model', notexist)
		if speed and not Processor.objects.filter(speed = speed):
			self.add_error('speed', notexist)



class RAMForm(ModelForm):
	prefix = 'ram'
	class Meta:
		model = RAM
		fields = [
		'model',
		'speed',
		]
	def __init__(self, *args, **kwargs):
		super(RAMForm, self).__init__(*args, **kwargs)
		self.fields['model'].required = False
		self.fields['model'].label = 'RAM Model'

		self.fields['speed'].required = False
		self.fields['speed'].label = 'RAM Speed'

	def clean(self):
		cleaned_data = super().clean()
		model = cleaned_data.get('model')
		speed = cleaned_data.get('speed')
		notexist = 'No such entries!'
		if model and not RAM.objects.filter(model__icontains = model):
			self.add_error('model', notexist)
		if speed and not RAM.objects.filter(speed = speed):
			self.add_error('speed', notexist)

class DiskForm(ModelForm):
	prefix = 'disk'
	class Meta:
		model = Disk
		fields = [
		'dtype',
		]
	def __init__(self, *args, **kwargs):
		super(DiskForm, self).__init__(*args, **kwargs)
		self.fields['dtype'].required = False
		self.fields['dtype'].label = 'Disk Type'

















