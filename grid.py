import pygame as pg
# import tkinter as tk
import pygame_gui
import PQ as pq
import itertools

# colors
background_color = (220, 220, 220)
outline_color = (166, 166, 186)
blue = (25, 45, 94)
green = (64, 156, 44)
gold = (201, 161, 38)
pink = (170, 120, 227)
light_green = (154, 237, 200)
dark_green = (9, 92, 55)
black = (0,0,0)
grid_standard_size = 25

selector_height = 100

pg.init()
screen_height = 600 + selector_height
screen_width = 600
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Path Finder")

background = pg.Surface(screen.get_size())
background.fill(background_color)  # fill the background white
background = background.convert()  # prepare for faster blitting
manager = pygame_gui.UIManager((screen_height, screen_width))

start_path_finding = pygame_gui.elements.UIButton(relative_rect=pg.Rect((screen_width - screen_width / 8 - 10,
                                                                         selector_height/4),
                                                                        (screen_width / 8, selector_height / 2)),
                                                  text='Start',
                                                  manager=manager)

restart = pygame_gui.elements.UIButton(relative_rect=pg.Rect((screen_width - screen_width / 4 - 30, selector_height/4),
                                                                        (screen_width / 8, selector_height/ 2)),
                                                  text='Restart',
                                                  manager=manager)

grid_size_selector_label = pygame_gui.elements.ui_label.UILabel(
    relative_rect=pg.Rect((screen_width / 4 + 60, selector_height / 8),
                          (screen_width / 4, selector_height / 4)),
    text="Select grid size",
    manager=manager)

grid_size_selector = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
    relative_rect=pg.Rect((screen_width / 4 + 60, selector_height/4 + selector_height/8),
                          (screen_width / 4, selector_height / 4)),
    start_value=2,
    value_range=(1, 3),
    manager=manager)

drop_down_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(relative_rect=pg.Rect((0, selector_height / 16),
                                                                                            (screen_width / 4,
                                                                                             selector_height / 4)),
                                                                      options_list=['start', 'end', 'wall'],
                                                                      starting_option='start',
                                                                      manager=manager)


class Pixel:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.width = pixel_width
        self.height = pixel_height
        self.vertex = pq.Vertex(self.i, self.j, self.i + self.j * grid_width)

    def draw(self, color, width_type):
        # draws a pixel of the grid
        pg.draw.rect(background, color, (self.i * self.width, self.j * self.height + selector_height, self.width,
                                         self.height), width_type)


def draw_vertex(vertex, color, width_type):
    # draws a pixel of the grid
    pg.draw.rect(background, color, (vertex.get_i() * pixel_width, vertex.get_j() * pixel_height + selector_height,
                                     pixel_width - 1, pixel_height - 1), width_type)


grid_height = screen_height - selector_height
grid_width = screen_width

# the following defines the width and height for a pixel
rows = grid_standard_size
cols = grid_standard_size
pixel_height = grid_width // rows
pixel_width = grid_width // cols

grid = []
g = pq.Graph()


def init_grid():
    global grid_height, grid_width, rows, cols, pixel_height, pixel_width, grid, background
    background.fill(background_color)  # fill the background white
    background = background.convert()  # prepare for faster blitting
    grid_height = screen_height - selector_height
    grid_width = screen_width
    # the following defines the width and height for a pixel
    rows = round(grid_size_selector.get_current_value()) * grid_standard_size
    cols = round(grid_size_selector.get_current_value()) * grid_standard_size
    pixel_height = grid_width // rows
    pixel_width = grid_width // cols
    grid = []

    # the following draws the grid system
    for _ in range(cols):
        # produce a 2d array that has 'cols' size and each index has an array that has size 'rows'
        grid.append([0 for j in range(rows)])

    for i in range(cols):
        for j in range(rows):
            pixel = Pixel(i, j)
            grid[i][j] = pixel
            g.add_vertex_by_obj(pixel.vertex)

    for i in range(cols):
        for j in range(rows):
            neighbours_index = grid[i][j].vertex.get_neighbours_index(grid_width, grid_height)
            for index in neighbours_index:
                neighbour = g.get_vertex(index[0] + index[1] * screen_width)
                if neighbour:
                    grid[i][j].vertex.add_neighbour(neighbour)
                    # print(g.get_vertex(grid[i][j].vertex.get_index()).get_neighbours())

            grid[i][j].draw(outline_color, 1)


init_grid()

mouse_type = drop_down_menu.selected_option
target_vertex = grid[cols - 1][rows - 1].vertex
start_vertex = grid[0][0].vertex


def mouse_to_pixel(mouse_pos):
    x = mouse_pos[0]
    y = mouse_pos[1] - selector_height

    pixel_x = (x - (x % pixel_height)) // pixel_height
    pixel_y = ((y - (y % pixel_height)) // pixel_height)
    # print(pixel_x, pixel_y)

    return pixel_x, pixel_y


def mouse_press(mouse_position):
    x, y = mouse_to_pixel(mouse_position)
    if 0 <= y < rows and 0 <= x < cols:
        # determine which pixel was pressed
        grid_index = grid[x][y].vertex.get_index()
        vertex = g.get_vertex(grid_index)
        if vertex:
            if drop_down_menu.selected_option == 'wall':
                grid[x][y].draw(black, 0)
                vertex.set_pixel_type('wall')

            elif drop_down_menu.selected_option == 'start':
                global start_vertex
                grid[start_vertex.get_i()][start_vertex.get_j()].draw(background_color, 0)
                grid[start_vertex.get_i()][start_vertex.get_j()].draw(outline_color, 1)
                grid[x][y].draw(gold, 0)
                start_vertex = vertex
                vertex.set_pixel_type('start')

            elif drop_down_menu.selected_option == 'end':
                global target_vertex
                grid[target_vertex.get_i()][target_vertex.get_j()].draw(background_color, 0)
                grid[target_vertex.get_i()][target_vertex.get_j()].draw(outline_color, 1)
                grid[x][y].draw((255,0,0), 0)
                target_vertex = vertex
                vertex.set_pixel_type('end')

        else:
            print("error changing pixel type")


def get_info(position):
    x, y = mouse_to_pixel(position)
    if 0 <= y < rows and 0 <= x < cols:
        # determine which pixel was pressed
        grid_index = grid[x][y].vertex.get_index()
        vertex = g.get_vertex(grid_index)
        if vertex:
            neighbours = vertex.get_neighbours()
            print('pixel', vertex.get_i(), vertex.get_j(), '| pixel type: ', vertex.get_pixel_type(),
                  'distance ', vertex.get_distance())
            if vertex.get_predecessor():
                print('predecessor: ', vertex.get_predecessor().get_i(), vertex.get_predecessor().get_j())
            else:
                print('no predecessor')
            for n in neighbours:
                print('neighbour', n.get_i(), n.get_j(), n.get_pixel_type(), 'neighbour_distance ', n.get_distance())
        else:
            print("error changing pixel type")


mainloop = True
mouse_dragging = False
dijkstra_go = False
clock = pg.time.Clock()
getTicksLastFrame = 0
draw_queue = []
draw_vertex_event = pg.USEREVENT + 1
pg.time.set_timer(draw_vertex_event, 1)
draw_path = False
path = []
restart_grid = False

while mainloop:
    time_delta = clock.tick(90) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            mainloop = False  # pygame window closed by user

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                mainloop = False  # user pressed ESC

        elif event.type == pg.MOUSEBUTTONDOWN:
            # if the left button is pressed
            if event.button == 1:
                mouse_position = pg.mouse.get_pos()
                mouse_dragging = True
                mouse_press(mouse_position)
            elif event.button == 3:
                mouse_position = pg.mouse.get_pos()
                get_info(mouse_position)

        elif event.type == pg.MOUSEBUTTONUP:
            # if the left button is pressedF
            if event.button == 1:
                mouse_dragging = False

        elif event.type == pg.MOUSEMOTION:
            # if the left button is pressed
            if mouse_dragging and drop_down_menu.selected_option == 'wall':
                mouse_position = pg.mouse.get_pos()
                mouse_dragging = True
                mouse_press(mouse_position)

        elif (event.type == pg.USEREVENT and
              event.user_type == pygame_gui.UI_BUTTON_PRESSED and
              event.ui_element == start_path_finding):
            dijkstra_go = True

        elif (event.type == pg.USEREVENT and
              event.user_type == pygame_gui.UI_BUTTON_PRESSED and
              event.ui_element == restart):
            restart_grid = True
            init_grid()

        elif event.type == pg.USEREVENT and grid_size_selector.has_moved_recently:
            dijkstra_go = False
            restart_grid = True
            init_grid()

        elif dijkstra_go:
            restart_grid = False
            start_vertex.set_distance(0)
            priority_queue = []
            entry_finder = {}
            counter = itertools.count()

            for value in g.get_vertices().values():
                pq.add_vertex(value, priority_queue, entry_finder, counter)

            while len(priority_queue):
                t = pg.time.get_ticks()
                deltaTime = (t - getTicksLastFrame) / 1000.0
                getTicksLastFrame = t
                current_v = pq.pop_vertex(priority_queue, entry_finder)
                if current_v.get_index() == target_vertex.get_index():
                    break
                if current_v is None:
                    break
                if current_v.visited or current_v.get_pixel_type() == 'wall':
                    current_v.set_visited()
                    continue
                current_v.set_visited()

                # check neighbour nodes of the current vertex
                neighbours = []
                for n in current_v.get_neighbours():
                    if not n.visited and (not n.get_pixel_type() == 'wall'):
                        neighbours.append(n)

                # add current vertex as the key and neighbours as value to a the draw queue
                draw_queue.append({current_v: neighbours})

                for neighbour in neighbours:
                    weight = pq.get_weight(current_v, neighbour)

                    if current_v.get_distance() + weight < neighbour.get_distance():
                        neighbour_in_graph = g.get_vertex(neighbour.get_index())
                        neighbour_in_graph.set_distance(current_v.get_distance() + weight)
                        neighbour_in_graph.set_predecessor(current_v)

                        # add entry to priority queue
                        pq.add_vertex(neighbour_in_graph, priority_queue, entry_finder, counter)

                        neighbour.set_distance(current_v.get_distance() + weight)
                        neighbour.set_predecessor(current_v)

            path = [target_vertex]
            pq.shortest(target_vertex, path)
            draw_path = True
            dijkstra_go = False

        elif event.type == draw_vertex_event:
            if restart_grid:
                draw_queue = []

            if len(draw_queue) and not restart_grid:
                current = draw_queue.pop(0)
                for vertex in current:
                    for neighbour in current[vertex]:
                        if neighbour.get_pixel_type() != 'start' and neighbour.get_pixel_type() != 'end':
                            draw_vertex(vertex=neighbour, color=dark_green, width_type=0)
                    if vertex.get_pixel_type() != 'start' and vertex.get_pixel_type() != 'end':
                        draw_vertex(vertex=vertex, color=light_green, width_type=0)
            elif draw_path and not restart_grid:
                # draws the shortest path
                for v in path:
                    if v.get_pixel_type() != 'start' and v.get_pixel_type() != 'end':
                        draw_vertex(vertex=v, color=blue, width_type=0)

        manager.process_events(event)

    manager.update(time_delta)

    # draw the contents of background
    screen.blit(background, (0, 0))

    manager.draw_ui(screen)

    pg.display.update()  # flip the screen like in a flipbook
