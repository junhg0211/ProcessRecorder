# coding=utf-8
import os
import datetime
import time
import pygame

class ProcessRecorder:
    @staticmethod
    def get_task_names():
        tasklist = os.popen('tasklist').read().split('\n')[2:-1]

        index_length = len(tasklist[0].split()[0])
        tasklist = tasklist[1:]

        task_names = []
        for i in range(len(tasklist)):
            task_name = tasklist[i][:index_length]
            if not task_name:
                continue

            while task_name[-1] == ' ':
                task_name = task_name[:-1]

            if task_name not in task_names:
                task_names.append(task_name)

        if 'tasklist.exe' in task_names:
            task_names.remove('tasklist.exe')

        return task_names

    def __init__(self, delay):
        self.delay = delay

        self.record_started_time = datetime.datetime.now()

        self.loop = time.time()
        self.ploop = self.loop

        self.running_tasks_times = {}
        self.gotten_tasks = []
        self.terminated_tasks_times = {}
        self.all_tasks = []

        self.gotten_tasks = []

    def get_session_length_all_the_time(self, filename) -> datetime.timedelta:
        length = datetime.timedelta()

        if filename in self.terminated_tasks_times.keys():
            length += self.terminated_tasks_times[filename]

        if filename in self.running_tasks_times.keys():
            length += (datetime.datetime.now() - self.running_tasks_times[filename])

        return length

    def aloop(self):
        previous_gotten_tasks = self.gotten_tasks
        self.gotten_tasks = ProcessRecorder.get_task_names()
        for gotten_task in self.gotten_tasks:
            if gotten_task not in self.all_tasks:
                self.all_tasks.append(gotten_task)
            if gotten_task not in previous_gotten_tasks:
                self.running_tasks_times[gotten_task] = datetime.datetime.now()

        for previous_gotten_task in previous_gotten_tasks:
            if previous_gotten_task not in self.gotten_tasks:
                session_length = (datetime.datetime.now() - self.running_tasks_times[previous_gotten_task])
                del self.running_tasks_times[previous_gotten_task]
                if previous_gotten_task in self.terminated_tasks_times.keys():
                    session_length += self.terminated_tasks_times[previous_gotten_task]

                self.terminated_tasks_times[previous_gotten_task] = session_length

pygame.init()

class root:
    class display:
        size = (480, 720)
        fps = 45

        pygame.display.set_caption('ProcessRecorder')
        pygame.display.set_icon(pygame.image.load('./res/image/icon.ico'))
    exit = False
    window = pygame.display.set_mode(display.size)

    clock = pygame.time.Clock()

class keyboard:
    lalt = False
    ralt = False

class cursor:
    wheel_up = False
    wheel_down = False

    position = pygame.mouse.get_pos()
    ppressed = pressed = pygame.mouse.get_pressed()
    fpressed = list(pressed)
    epressed = list(pressed)

class color:
    background = (252, 250, 223)
    text = (31, 18, 0)

    slider_background = (96, 76, 88)
    slider_button = (42, 36, 39)

class TextFormat:
    def __init__(self, font, size, colour):
        self.font = font
        self.size = size
        self.colour = colour

        self.font = pygame.font.Font(font, size)

    def render(self, text):
        return self.font.render(text, True, self.colour)

class RootObject:
    objects = []

    @staticmethod
    def add(obj):
        RootObject.objects.append(obj)

    def tick(self):
        pass

    def render(self):
        pass

    def destory(self):
        if self in RootObject.objects:
            RootObject.objects.remove(self)

class Text(RootObject):
    def __init__(self, x, y, text, text_format):
        self.x = x
        self.y = y
        self.text = text
        self.text_format = text_format

        self.surface = self.text_format.render(self.text)

    def render(self):
        root.window.blit(self.surface, (self.x, self.y))

def center(x, y):
    return (x - y) / 2

class Clock(RootObject):
    def __init__(self, list_object):
        self.now = datetime.datetime.now()

        self.date = ''
        self.time = ''
        self.seconds = ''
        self.start = str(list_object.process_recorder.record_started_time)

        self.date_text_format = TextFormat('./res/font/NotoSansCJKkr-Regular.otf', 24, color.text)
        self.time_text_format = TextFormat('./res/font/NotoSansCJKkr-Regular.otf', 72, color.text)
        self.seconds_text_format = TextFormat('./res/font/NotoSansCJKkr-DemiLight.otf', 20, color.text)
        self.start_text_format = TextFormat('./res/font/NotoSansCJKkr-DemiLight.otf', 12, color.text)

        self.date_surface = pygame.Surface((0, 0))
        self.time_surface = pygame.Surface((0, 0))
        self.seconds_surface = pygame.Surface((0, 0))
        self.start_surface = self.start_text_format.render(self.start)

        self.date_position = [0, 57]
        self.time_position = [0, 66]
        self.seconds_position = [269, 147]
        self.start_position = [center(root.display.size[0], self.start_surface.get_width()), 195]

    def update(self):
        self.now = datetime.datetime.now()

        self.date = '%04d-%02d-%02d' % (self.now.year, self.now.month, self.now.day)
        self.time = '%d:%02d' % (self.now.hour, self.now.minute)
        self.seconds = f':{self.now.second}.{self.now.microsecond}'

    def tick(self):
        self.update()

        self.date_surface = self.date_text_format.render(self.date)
        self.time_surface = self.time_text_format.render(self.time)
        self.seconds_surface = self.seconds_text_format.render(self.seconds)

        self.date_position[0] = center(root.display.size[0], self.date_surface.get_width())
        self.time_position[0] = center(root.display.size[0], self.time_surface.get_width())

    def render(self):
        root.window.blit(self.date_surface, self.date_position)
        root.window.blit(self.time_surface, self.time_position)
        root.window.blit(self.seconds_surface, self.seconds_position)
        root.window.blit(self.start_surface, self.start_position)

def bound(value, minv, maxv):
    if value < minv:
        return minv
    elif value > maxv:
        return maxv
    else:
        return value

program_name_text_format = TextFormat('./res/font/NotoSansCJKkr-Medium.otf', 24, color.text)
elapsed_time_text_format = TextFormat('./res/font/NotoSansCJKkr-Thin.otf', 16, color.text)

class List(RootObject):
    class Index(RootObject):
        def __init__(self, program_name, parent):
            self.program_name = program_name
            self.parent = parent

            self.program_name_surface = program_name_text_format.render(program_name)

            self.elapsed_time = ''
            self.elapsed_time_surface = pygame.Surface((0, 0))

            self.y = 0

        def tick(self):
            self.y = self.parent.list_length - \
                     (list(self.parent.indexes.values()).index(self) * 65 + self.parent.y) + 200

            self.elapsed_time = str(self.parent.times[self.program_name])
            self.elapsed_time_surface = elapsed_time_text_format.render(self.elapsed_time)

        def render(self):
            if bound(self.y, 236, 700) == self.y:
                root.window.blit(self.program_name_surface, (22, self.y))

            y2 = self.y + 25

            if bound(y2, 244, 700) == y2:
                root.window.blit(self.elapsed_time_surface, (22, y2))

    def __init__(self):
        self.process_recorder = ProcessRecorder(1)

        self.count = 0
        self.times = {}
        self.indexes = {}

        self.y = 0
        self.y_target = 0
        self.list_length = 0
        self.slider_button_height = 0
        self.slider_button_y = 259

        self.fpressed_position = []
        self.clicked_y_moving = False

    def tick(self):
        if self.count > 0:
            self.count -= 1
        else:
            self.count = root.display.fps
            self.process_recorder.aloop()

            for task in self.process_recorder.all_tasks:
                self.times[task] = self.process_recorder.get_session_length_all_the_time(task)

            self.list_length = 65 * len(self.times.values())
            self.slider_button_height = 431 / self.list_length * 259

            for taskname in self.times.keys():
                if taskname not in self.indexes.keys():
                    self.indexes[taskname] = self.Index(taskname, self)

        if self.y_target != self.y:
            self.y += (self.y_target - self.y) / (240 / root.display.fps)
            if abs(self.y - self.y_target) < 0.01:
                self.y = self.y_target
            self.slider_button_y = self.y / (self.list_length - 431) * (431 - self.slider_button_height) + 259

        if cursor.wheel_down:
            self.y_target += 195
        elif cursor.wheel_up:
            self.y_target -= 195

        self.y_target = bound(self.y_target, 0, self.list_length - 431)

        dictionary = {}
        for key in sorted(self.indexes)[::-1]:
            dictionary[key] = self.indexes[key]
        self.indexes = dictionary

        if cursor.fpressed[0] and bound(cursor.position[0], 460, 470) == cursor.position[0] and \
                bound(cursor.position[1], self.slider_button_y, self.slider_button_y + self.slider_button_height):
            self.clicked_y_moving = True

        if self.clicked_y_moving:
            self.y_target = bound((cursor.position[1] - 259) / 431, 0, 1) * (self.list_length - 431)

            if cursor.epressed[0]:
                self.clicked_y_moving = False

        for index in self.indexes.values():
            index.tick()

    def render(self):
        pygame.draw.rect(root.window, color.slider_background, ((460, 259), (10, 431)))
        pygame.draw.rect(root.window, color.slider_button,
                         ((460, self.slider_button_y), (10, self.slider_button_height)))

        for index in self.indexes.values():
            index.render()

class GaroLine(RootObject):
    def __init__(self, y, colour=color.text):
        self.y = y
        self.colour = colour

    def render(self):
        pygame.draw.line(root.window, self.colour, (0, self.y), (root.display.size[0], self.y))

def tick():
    for i in range(3):
        cursor.fpressed[i] = not cursor.ppressed[i] and cursor.pressed[i]
        cursor.epressed[i] = cursor.ppressed[i] and not cursor.pressed[i]

def main():
    list_o = List()
    RootObject.add(list_o)
    RootObject.add(Clock(list_o))

    while not root.exit:
        cursor.position = pygame.mouse.get_pos()
        cursor.ppressed = cursor.pressed
        cursor.pressed = pygame.mouse.get_pressed()
        cursor.wheel_up = False
        cursor.wheel_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                root.exit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    cursor.wheel_up = True
                elif event.button == 5:
                    cursor.wheel_down = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT:
                    keyboard.lalt = True
                elif event.key == pygame.K_RALT:
                    keyboard.ralt = True
                elif event.key == pygame.K_F4:
                    if keyboard.lalt or keyboard.ralt:
                        root.exit = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LALT:
                    keyboard.lalt = False
                elif event.key == pygame.K_RALT:
                    keyboard.ralt = False

        tick()
        for obj in RootObject.objects:
            obj.tick()

        root.window.fill(color.background)
        for obj in RootObject.objects:
            obj.render()
        pygame.display.flip()

        root.clock.tick(root.display.fps)
    pygame.quit()

if __name__ == '__main__':
    main()
