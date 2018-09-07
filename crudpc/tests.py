from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.http import urlencode
import shutil

from .models import Computer, Processor, RAM, Disk


def create_processor(model, speed):
    cpu = Processor.objects.create(model=model, speed=speed)
    return cpu


def create_ram(model, speed):
    ram = RAM.objects.create(model=model, speed=speed)
    return ram


def create_disk(dtype):
    disk = Disk.objects.create(dtype=dtype)
    return disk


def create_computer(processor=None, ram=None, disk=None):
    if not processor:
        processor = create_processor('Celeron 1', 1200)
    if not ram:
        ram = create_ram('SupeRAM', 1333)
    if not disk:
        disk = create_disk('HDD')
    testimage = SimpleUploadedFile(name='test_image.png', content=open('crudpc/testimg/fake.png', 'rb').read(),
                                   content_type='image/png')

    pc = Computer.objects.create(processor=processor, ram=ram, disk=disk, photo=testimage)
    return pc


###cpu-model=i7+45&cpu-speed=&ram-model=&ram-speed=&disk-dtype=

class ShowListingViewTests(TestCase):
    def test_show_pc_regular(self):
        # just create a pc and check if it appeared in the listing
        pc = create_computer()
        response = self.client.get(reverse('listing'))
        self.assertContains(response, pc.processor)
        self.assertContains(response, pc.ram)

    def test_not_show_pc_deleted(self):
        # create a pc, then delete it from the database and check if it appeared in the listing (it should not)
        pc = create_computer()
        cpu = pc.processor
        ram = pc.ram
        disk = pc.disk
        pc.delete()
        response = self.client.get(reverse('listing'))
        # for line in response.content.decode('UTF-8').split('\n'):
        #   if "HDD" in line:
        #       print('here!', line)
        self.assertNotContains(response, cpu)
        self.assertNotContains(response, ram)

    def test_show_pc_filtered(self):
        # create a pc, then filter for its data and assert it shows
        pc = create_computer()
        getParams = urlencode({
            'cpu-model': pc.processor.model,
            'cpu-speed': pc.processor.speed,
            'ram-model': pc.ram.model,
            'ram-speed': pc.ram.speed,
            'disk-dtype': pc.disk.dtype,
        })
        # print(getParams)
        response = self.client.get(reverse('listing') + '?' + getParams)
        self.assertContains(response, pc.processor)
        self.assertContains(response, pc.ram)

    def test_not_show_pc_filtered(self):
        # create two pcs with different components, then use a filter which shouldn't have a match. assert doesn't show
        pc1 = create_computer(processor=create_processor('intel', 2000), ram=create_ram('Samsung', 1400))
        pc2 = create_computer(processor=create_processor('amd', 1999), ram=create_ram('Kingston', 1500))
        getParams = urlencode({
            'cpu-model': pc1.processor.model,
            'cpu-speed': pc1.processor.speed,
            'ram-model': pc2.ram.model,
            'ram-speed': pc2.ram.speed,
        })
        response = self.client.get(reverse('listing') + '?' + getParams)
        self.assertQuerysetEqual(response.context['computers'], [])

    def test_show_input_error_no_entries(self):
        # create a pc then filter using one or more component attributes which don't exist in the database
        pc = create_computer()
        notexist = 'No such entries!'
        getParams = urlencode({
            'cpu-model': 'not existing model',
            'cpu-speed': pc.processor.speed,
            'ram-model': pc.ram.model,
            'ram-speed': pc.ram.speed,
        })
        response = self.client.get(reverse('listing') + '?' + getParams)
        self.assertContains(response, notexist)


class AddViewTests(TestCase):
    def test_add_pc_regular(self):
        pass
