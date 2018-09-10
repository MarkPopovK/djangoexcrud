from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.http import urlencode
import shutil, os
import tempfile
from django.conf import settings

settings.MEDIA_ROOT += 'test/'

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


def create_photo(empty=True):
    if empty:
        testimage = tempfile.NamedTemporaryFile(suffix=".jpg").name
    else:
        testimage = SimpleUploadedFile(name='test_image.png', content=open('crudpc/testimg/fake.png', 'rb').read(),
                                       content_type='image/png')
    return testimage


def create_computer(processor=None, ram=None, disk=None):
    if not processor:
        processor = create_processor('Celeron 1', 1200)
    if not ram:
        ram = create_ram('SupeRAM', 1333)
    if not disk:
        disk = create_disk('HDD')

    testimage = create_photo()

    pc = Computer.objects.create(processor=processor, ram=ram, disk=disk, photo=testimage)
    return pc



###

class ShowListingViewTests(TestCase):
    def test_show_pc_regular(self):
        # just create a pc and check if it appeared in the listing
        pc = create_computer()
        response = self.client.get(reverse('listing'))
        self.assertContains(response, pc.processor)
        self.assertContains(response, pc.ram)

    def test_not_show_pc_deleted(self):
        # create a pc, then delete it from the database and check if it appeared in the listing
        pc = create_computer()
        pc.delete()
        response = self.client.get(reverse('listing'))
        # for line in response.content.decode('UTF-8').split('\n'):
        #     if "Celeron" in line:
        #         print('here!', line)
        self.assertQuerysetEqual(response.context['computer_list'], [])

    def test_show_pc_filtered(self):
        # create a pc, then filter for its data and assert it shows
        pc = create_computer()
        getparams = {
            'pc-processor': pc.processor.id,
            'pc-ram': pc.ram.id,
            'pc-disk': pc.disk.id,
        }
        # print(getParams)
        response = self.client.get(reverse('listing'), getparams)
        self.assertContains(response, pc.processor)
        self.assertContains(response, pc.ram)

    def test_not_show_pc_filtered(self):
        # create two pcs with different components, then use a filter which shouldn't have a match. assert doesn't show
        pc1 = create_computer(processor=create_processor('intel', 2000), ram=create_ram('Samsung', 1400))
        pc2 = create_computer(processor=create_processor('amd', 1999), ram=create_ram('Kingston', 1500))
        getParams = urlencode({
            'pc-processor': pc1.processor.id,
            'pc-ram': pc2.ram.id,
            'pc-disk': pc1.disk.id,
        })
        response = self.client.get(reverse('listing') + '?' + getParams)
        self.assertQuerysetEqual(response.context['computer_list'], [])

    # def test_show_input_error_no_entries(self):
    #     # create a pc then filter using one or more component attributes which don't exist in the database
    #     pc = create_computer()
    #     notexist = 'No such entries!'
    #     getParams = urlencode({
    #         'cpu-model': 'not existing model',
    #         'cpu-speed': pc.processor.speed,
    #         'ram-model': pc.ram.model,
    #         'ram-speed': pc.ram.speed,
    #     })
    #     response = self.client.get(reverse('listing') + '?' + getParams)
    #     self.assertContains(response, notexist)


class AddViewTests(TestCase):
    def tearDown(self):
        if 'test' in settings.MEDIA_ROOT and os.path.exists(settings.MEDIA_ROOT):
            shutil.rmtree(settings.MEDIA_ROOT)

    def test_add_pc_regular(self):
        # create a pc via post request and check if it gets into the database
        cpu = create_processor('cpumodel1', 2900)
        ram = create_ram('RAMzes', 2000)
        disk = create_disk('HDD')
        self.assertEqual(Computer.objects.all().count(), 0)
        with create_photo(empty=False) as fp:
            self.client.post(reverse('add'),
                             {'processor': cpu.pk,
                              'ram': ram.pk,
                              'disk': disk.pk,
                              'photo': fp})
        self.assertEqual(Computer.objects.all().count(), 1)

    def test_add_pc_nonvalid(self):
        # create a pc with not valid data
        cpu = create_processor('cpumodel1', 2900)
        ram = create_ram('RAMzes', 2000)
        disk = create_disk('HDD')
        self.assertEqual(Computer.objects.all().count(), 0)
        with create_photo(empty=False) as fp:
            self.client.post(reverse('add'),
                             {'processor': 'invalid-cpu',
                              'ram': ram.pk,
                              'disk': disk.pk,
                              'photo': fp})
        self.assertEqual(Computer.objects.all().count(), 0)


class EditViewTests(TestCase):
    def test_edit_pc_regular(self):
        # create a pc, assing it a cpu, change it via post request, check if it has changed in the database
        cpu1 = create_processor('cpumodel1', 2900)
        pc = create_computer(processor=cpu1)
        self.assertEqual(Computer.objects.all()[0].processor.model, "cpumodel1")
        cpu2 = create_processor('cpumodel2', 3300)
        self.client.post(reverse('edit', args=[pc.pk]),
                         {'processor': cpu2.pk,
                          'ram': pc.ram.pk,
                          'disk': pc.disk.pk, })
        self.assertEqual(Computer.objects.all()[0].processor.model, "cpumodel2")

class RemoveViewTests(TestCase):
    def test_remove_pc_regular(self):
        # create a pc, delete it via post request, check if deleted
        pc = create_computer()
        self.assertEqual(Computer.objects.all().count(), 1)
        self.client.post(reverse('remove', args=[pc.pk]))
        self.assertEqual(Computer.objects.all().count(), 0)
