
from tkinter import Tk, Canvas,Label,IntVar,Scale,Button,StringVar,OptionMenu,HORIZONTAL,font,PhotoImage, BooleanVar
    
from PIL import Image, ImageTk
from generate_image import image_generator

class ImageGenerationGUI:
    def __init__(self, w=850, h=410):
        self.root = Tk()
        #print(self.birds_attribute_types)
        self.celebs_attribute_values = [['Yes', 'No'], ['Yes', 'No'], ['Male', 'Female']]
        self.celebs_attribute_types = ['Has eyeglasses', 'Is young', 'Sex']
        self.num_iters = len(self.celebs_attribute_types)
        self.curr_scale_vals = [self.celebs_attribute_values[i][0] for i in range(self.num_iters)]
        self.w = w
        self.h = h
        self.offx = 5
        self.offy = 5
        self.imagew = 300
        self.imageh = 300
        self.curr_dataset = 'Birds'
        self.root.title("CGAN Image Generator")
    
        self.dataset_names = {'Birds' :-1}
        self.dataset_names['Celebrities'] = 0
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (self.w / 2)
        y = (hs / 2) - (self.h / 2)
        
        self.root.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
        self.draw_image()
        self.draw_configurations()

    def on_option_selected(self, *args):
     #   print("Selected option:", self.option_menus_var.get())
        dataset_before = self.curr_dataset
        self.curr_dataset = self.option_menus_var.get()
        if dataset_before != self.curr_dataset:
            if dataset_before == "Birds":
                self.dropdown_menu.grid_remove()
                for i in range(len(self.labels)):
                    self.labels[i].grid()
                    self.scales[i].grid()
            else:
                for i in range(len(self.labels)):
                    self.labels[i].grid_remove()
                    self.scales[i].grid_remove()
                self.dropdown_menu.grid()
        


    def on_dropdown_change(self, *args):
        self.selected_bird = self.dropdown_menu_var.get()
        print("Selected bird:", self.selected_bird)
        
    def draw_configurations(self):
        self.configuration = Canvas(self.root, height=self.h - self.imageh, width=self.w - self.imagew)
        self.configuration.pack(side="left")
        self.scale_vars = []
        self.labels_dict = {}
        num_iters = self.num_iters
        self.scale_vars = [IntVar() for _ in range(num_iters)]
        self.labels = [Label(self.configuration, 
                             text=f"{self.celebs_attribute_types[i]}: {self.celebs_attribute_values[i][0]}") 
                             for i in range(num_iters)]
        self.scales = []
        for i in range(num_iters):
            scale_var = IntVar()
            self.scale_vars.append(scale_var)
            scale = Scale(self.configuration, variable=self.scale_vars[i], 
                          command=lambda value, idx=i: self.slider_value_change_handler(value, self.labels[idx]), 
                          from_=0, to=len(self.celebs_attribute_values[i]) - 1, resolution=1, width="15", 
                          orient=HORIZONTAL, length="200", showvalue=0)
            scale.set(0)
            scale.grid(row=0, column=0, padx=(10, 0), pady=(0, ((i) * 2 + 1)*40 + 80))
            self.scales.append(scale)
            self.labels[i].grid(row=0, column=0, padx=(10, 0), pady=(0, (2 * (i))*40 + 80))

        for i in range(len(self.labels)):
            self.labels[i].grid_remove()
            self.scales[i].grid_remove()
        # Options for the dropdown menu
        self.bird_options = ["Yellow headed Blackbird", "Indigo Bunting", "Painted Bunting",
                             "Cardinal", "Spotted Catbird", "Gray Catbird", "Yellow breasted Chat",
                             "American Crow", "Vermilion Flycatcher", "American Goldfinch"]

        self.dropdown_menu_var = StringVar(self.root)
        self.dropdown_menu_var.set(self.bird_options[0])
        self.dropdown_menu = OptionMenu(self.configuration, self.dropdown_menu_var, 
                                      *self.bird_options, command = self.on_dropdown_change)
        self.dropdown_menu.grid(row=0, column=0, padx=(10, 0), pady=(0, 265))
        self.dropdown_menu.config(width=20)
        self.selected_bird = self.bird_options[0]
        #self.dropdown_menu.grid_remove()

        

        self.button = Button(self.configuration, text="Generate Image", width="20", height="2",
                              command=self.generate_image_button_click_handler)
        self.button['font'] = ("Helvetica", 12)
        self.button.grid(row=0, column=0, columnspan=1, pady=(255, 0))

        label = Label(self.configuration, text="Current dataset")
        label.grid(row=0, column = 1, padx=(10, 0), pady=(0, 280))
        self.option_menus_var = StringVar(self.root)
        self.option_menus_var.set(self.curr_dataset)
        self.option_menu = OptionMenu(self.configuration, self.option_menus_var, 
                                      *self.dataset_names, command = self.on_option_selected)
        self.option_menu.grid(row=0, column=1, padx=(10, 0), pady=(0, 210))
        self.option_menu.config(width=10)

    def toggle_dropdown(self):
        if self.show_dropdown.get():
            self.dropdown_menu.grid()
        else:
            self.dropdown_menu.grid_remove()
        self.show_dropdown.set(not self.show_dropdown.get())

    def draw_image(self):
        self.grid = Canvas(self.root, height=self.imageh, width=self.imagew)
        self.grid.pack(side="left")

        original_image = Image.open("example.png")
        resized_image = original_image.resize((300, 300), Image.ANTIALIAS)

        self.image = ImageTk.PhotoImage(resized_image)
        self.image_label = Label(self.grid, image=self.image)
        self.image_label.pack(side="left")
    
    def slider_value_change_handler(self, value, label):
        str_label = str(label)
        slider_type = str_label[-1]
        if str_label[-1] == 'l':
            slider_type = 0
        else:
            slider_type = int(slider_type) - 1
        attr_val = self.birds_attribute_values[slider_type][int(value)]
        attr_type = self.birds_attribute_types[slider_type]
        text = f"{attr_type}: {attr_val}"
        label.config(text=text)
        self.curr_scale_vals[slider_type] = self.birds_attribute_values[slider_type][self.scale_vars[slider_type].get()]

    def get_image(self):
        selected_class = 0
        if self.curr_dataset == "Birds":
            idx = self.bird_options.index(self.selected_bird)
            print(idx, selected_class)
            selected_class = idx + 1
        else:
            for i in range(len(self.scale_vars)):
                selected_class += self.scale_vars[i].get() * 2 ** (i)          

        image = image_generator(self.curr_dataset, selected_class)
        return image
       
    def generate_image_button_click_handler(self):
        image = self.get_image()
        original_image = Image.fromarray(image.astype('uint8'))
        resized_image = original_image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo 

if __name__ == "__main__": 

    gui = ImageGenerationGUI()
    gui.root.mainloop()