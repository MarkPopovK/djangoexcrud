# from django.db import models

# class Computer(models.Model):
# 	processorModel	= models.CharField(max_length = 100)
# 	processorSpeed	= models.IntegerField() # MHz ex. 2800
# 	ramModel		= models.CharField(max_length = 100)
# 	ramSpeed		= models.IntegerField() # MHz ex. 1333
# 	possibleDiskTypes = (
# 		('HDD', 'HDD'),
# 		('SSD', 'SSD'))
# 	diskType		= models.CharField(max_length = 100, choices = possibleDiskTypes)
# 	photo			= models.ImageField()

# 	def __str__(self):
# 		describe = f'{self.processorModel} ({self.processorSpeed}MHz), {self.ramModel} ({self.ramSpeed}MHz), {self.diskType}'
# 		return describe

from django.db import models

class Processor(models.Model):
	model = models.CharField(max_length = 100)
	speed = models.IntegerField() # MHz ex. 2800
	def __str__(self):
		return f'{self.model} ({self.speed}MHz)'

class RAM(models.Model):
	model = models.CharField(max_length = 100)
	speed = models.IntegerField() # MHz ex. 1333
	def __str__(self):
		return f'{self.model} ({self.speed}MHz)'

class Disk(models.Model):
	possibleDiskTypes = (
		('', ''),
		('HDD', 'HDD'),
		('SSD', 'SSD'))
	dtype = models.CharField(max_length = 100, choices = possibleDiskTypes, default = 'HDD')
	def __str__(self):
		return f'{self.dtype}'

class Computer(models.Model):
	processor =	models.ForeignKey('Processor', on_delete = models.SET_NULL, blank = True, null = True)
	ram =		models.ForeignKey('RAM', on_delete = models.SET_NULL, blank = True, null = True)
	disk =		models.ForeignKey('Disk', on_delete = models.SET_NULL, blank = True, null = True)
	photo =		models.ImageField()

	def __str__(self):
		describe = f'{self.processor}, {self.ram}, {self.disk}'
		return describe

	def html_describe(self):
		describe = f'''\
		CPU: {self.processor}
		RAM: {self.ram}
		DISK: {self.disk}'''
		return describe













# Create your models here.
