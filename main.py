import tkinter as tk 
import math 

def penalty_time():
    pass

def access_time():
    pass

def hex_to_binary(hex, mem_size, kb_or_mb):
    if kb_or_mb == 'kb':
        size = math.log(mem_size * 1024, 2)
    else:
        size = math.log(mem_size * 1024 * 1024, 2)
    binary = str(bin(int(hex[2:], 16))[2:].zfill(int(size)))[-int(size):]
    return binary

def tag_index_offset(binary, block_size, cache_size, cache_kb_or_mb):
    full_length = len(binary)
    if cache_kb_or_mb == 'kb':
        cache_size = cache_size * 1024
    else:
        cache_size = cache_size * 1024 * 1024
    offset_length = math.log(block_size, 2)
    index_length = math.log(cache_size/block_size, 2)
    tag_length = full_length - (offset_length + index_length)
    return [int(tag_length), int(index_length), int(offset_length)]

def main():
    index_tag_dict = {}
    hits, misses=0, 0

    def step_pressed():
        binary = hex_to_binary(entry_list['hex address:'].get(), int(entry_list['memory size:'].get()), mem_var)
        tag_index_offset_list = tag_index_offset(binary, int(entry_list['block size:'].get()), int(entry_list['cache size:'].get()), cache_var.get())
        tag = binary[0:tag_index_offset_list[0]]
        index = binary[tag_index_offset_list[0]:tag_index_offset_list[0] + tag_index_offset_list[1]]
        offset = binary[tag_index_offset_list[0] + tag_index_offset_list[1]: tag_index_offset_list[0] + tag_index_offset_list[1] + tag_index_offset_list[2]]
        binary_var = tk.StringVar()
        binary_var.set(tag + " " + index + " " + offset)
        entry_list['binary address:'].configure(textvariable = binary_var)
        if index in index_tag_dict:
            if index_tag_dict[index] == tag:
                hit_or_miss = "Hit"
                hits += 1
            else:
                hit_or_miss = "Miss"
                index_tag_dict[index] = tag
                misses += 1
        else:
            hit_or_miss = "Miss"
            index_tag_dict[index] = tag
            misses += 1

        hit_or_miss_var = tk.StringVar()
        hit_or_miss_var.set(hit_or_miss)
        entry_list['hit or miss:'].configure(textvariable = hit_or_miss_var)
        
    def cacl_pressed():
        pass

    def res_pressed():
        nonlocal index_tag_dict, hits, misses
        index_tag_dict = {}
        hits, misses = 0, 0
        for key in entry_list:
            var = tk.StringVar()
            var.set('')
            entry_list[key].configure(textvariable = var)
        

    window = tk.Tk()
    window.title("Direct mapping simulator")
    window.geometry("600x600")
    window.resizable(False, False)

    btn_calc = tk.Button(master = window, text = "calculate", command = None, highlightbackground='black', relief='raised')
    btn_step = tk.Button(master = window, text = 'step', command = step_pressed, highlightbackground='black', relief='raised')
    btn_res = tk.Button(master = window, text = "reset", command = res_pressed, highlightbackground='black', relief='raised')
    
    labels_names = ['memory size:', 'cache size:', 'block size:', 'hex address:', 'cache miss penalty time:', 'cache access time:', 'hit or miss:', 'binary address:']
    entry_list = {}
    for i in labels_names:
        label = tk.Label(master=window, text=i, font=(None, 15))
        x = 15
        y = 60*labels_names.index(i)+30
        label.place(x=x,y=y)
        entry_list[i] = tk.Entry(master = window, width = 15)
        entry_list[i].place(x=x+260,y=y)
        if i == 'cache access time:' or i == 'binary address:' or i == 'hit or miss:':
            entry_list[i].config(state = 'disabled')
        if i == 'cache miss penalty time:':
            ns_label = tk.Label(master = window, text='ns', font=(None,15))
            ns_label.place(x=430,y=y)
            ns_label = tk.Label(master = window, text='ns', font=(None,15))
            ns_label.place(x=430,y=y+60)

    entry_list['binary address:'].config(width = 35)

    btn_step.place(x=x, y=510)
    btn_calc.place(x=x+70, y=510)
    btn_res.place(x=x+170, y=510)

    mem_var = tk.StringVar()
    mem_var.initialize("kb")
    mg_radio = tk.Radiobutton(master = window, text = "MB", variable = mem_var, value = 'mb')
    kb_radio = tk.Radiobutton(master = window, text = "KB", variable = mem_var, value = 'kb')
    mg_radio.place(x=500,y=30)
    kb_radio.place(x=430,y=30)

    cache_var = tk.StringVar()
    cache_var.initialize('kb')
    mg_radio = tk.Radiobutton(master = window, text = "MB", variable = cache_var, value = 'mb')
    kb_radio = tk.Radiobutton(master = window, text = "KB", variable = cache_var, value = 'kb')
    mg_radio.place(x=500,y=90)
    kb_radio.place(x=430,y=90)

    block_var = tk.StringVar()
    block_var.initialize('B')
    b_radio = tk.Radiobutton(master = window, text = "B", variable = block_var, value = "B")
    b_radio.place(x=430, y=150)

    entry_list['memory size:'].focus()
    window.mainloop()

main()
