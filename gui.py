import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import pandas as pd
from nltk import tokenize
import numpy as np

with open("view_complete.pkl", "rb") as f:
    view_complete = pickle.load(f)

# with open("definition_labelencoder.pkl", "rb") as f:
#     definition_labelencoder = pickle.load(f)

# with open("country_labelencoder.pkl", "rb") as f:
#     country_labelencoder = pickle.load(f)

def generate_tags(data, generated_tags_lst, depth=10, cur_depth=0):
    if depth == cur_depth:
        # messagebox.showinfo("Form Submitted", f"Data Submitted:\n{data}")
        return
    
    changes = {"no change": view_complete.predict(pd.DataFrame([data]))}
    datas = []
    y = []
    for column in data:
        if column.startswith("tag_"):
            if data[column] != 1:
                data[column] = 1
                # changes[column] = view_complete.predict(pd.DataFrame([data]))
                # data[column] = 0

                datas.append(data.copy())
                y.append(column)
                data[column] = 0

    y_pred = view_complete.predict(pd.DataFrame(datas))
    for i in range(len(y)):
        changes[y[i]] = y_pred[i]

    # find key with max value in change
    max_change = max(changes, key=changes.get)
    if max_change == "no change":
        # messagebox.showinfo("Form Submitted", f"Data Submitted:\n{data}")
        # messagebox.showinfo("Predictions", f"Predictions:\n{view_complete.predict(pd.DataFrame([data]))}")
        return
    
    data[max_change] = 1
    generated_tags_lst.append(max_change)
    generate_tags(data, generated_tags_lst, depth, cur_depth+1)
    

def submit_form():
    # Gather data from the form
    data = {
        "Category": category_var.get(),
        "Title": title_var.get(),
        "Description": description_var.get(),
        "Tags": tags_var.get(),
        "Comments Disabled": comments_disabled_var.get(),
        "Region": region_var.get(),
        "Duration (seconds)": duration_var.get(),
        "Definition": definition_var.get(),
        "Caption": caption_var.get(),
        "Comment Sentiment": sentiment_var.get(),
        "Subscribers": subscribers_var.get()
    }

    category_id = categories_id_map[data["Category"]]
    definition_id = 0 if data["Definition"] == "HD" else 1
    country_id = regions.index(data["Region"])

    title_words = set(tokenize.word_tokenize(data["Title"].lower()))
    description_words = set(tokenize.word_tokenize(data["Description"].lower()))
    cur_tags = set(data["Tags"].lower().split(", "))

    cur_tags = cur_tags.intersection(all_tags)
    title_words = title_words.intersection(all_tags)
    description_words = description_words.intersection(all_tags)

    current_tags = cur_tags.union(title_words).union(description_words)

    data = {
        "categoryId": category_id,
        "comments_disabled": bool(data["Comments Disabled"]),
        "region": country_id,
        "duration": data["Duration (seconds)"],
        "definition": definition_id,
        "caption": bool(data["Caption"]),
        "comment_sentiment": data["Comment Sentiment"],
        "subscribers": data["Subscribers"],
    }

    for tag in tags:
        data[tag] = 0

    for tag in current_tags:
        data[f"tag_{tag}"] = 1

    data["log_duration"] = np.log(data["duration"])

    # print("\n".join(list(data.keys())))

    generated_tags_lst = []
    generate_tags(data, generated_tags_lst)

    # Display the collected data (or handle it as needed)
    # messagebox.showinfo("Predictions", f"Predictions:\n{view_complete.predict(pd.DataFrame([data]))[0]}")
    generated_tags_label.config(text=f"Generated Tags: {', '.join([i[4:] for i in generated_tags_lst])}")
    if data["subscribers"] <= 100000:
        predicted_views = int(15463 * np.log(data["subscribers"] if data["subscribers"] > 0 else 10))
    elif 100000 <= data["subscribers"] <= 10000000:
        predicted_views = int(view_complete.predict(pd.DataFrame([data]))[0]) // 10
    else:
        predicted_views = int(view_complete.predict(pd.DataFrame([data]))[0])
    # format views in Million and K
    if predicted_views >= 1000000:
        predicted_views = f"{predicted_views/1000000:.2f}M"
    elif predicted_views >= 1000:
        predicted_views = f"{predicted_views/1000:.2f}K"
    predicted_subscribers_label.config(text=f"Predicted Views: {str(predicted_views)}")

# Initialize the main window
root = tk.Tk()
root.title("Video Information Form")
root.geometry("500x700")

# Variables for storing form data
category_var = tk.StringVar()
title_var = tk.StringVar()
description_var = tk.StringVar()
tags_var = tk.StringVar()
comments_disabled_var = tk.BooleanVar()
region_var = tk.StringVar()
duration_var = tk.IntVar()
definition_var = tk.StringVar()
caption_var = tk.BooleanVar()
sentiment_var = tk.DoubleVar()
subscribers_var = tk.IntVar()

category_mapping = {
    2: "Autos & Vehicles",
    1: "Film & Animation",
    10: "Music",
    15: "Pets & Animals",
    17: "Sports",
    18: "Short Movies",
    19: "Travel & Events",
    20: "Gaming",
    21: "Videoblogging",
    22: "People & Blogs",
    23: "Comedy",
    24: "Entertainment",
    25: "News & Politics",
    26: "Howto & Style",
    27: "Education",
    28: "Science & Technology",
    29: "Nonprofits & Activism",
    30: "Movies",
    31: "Anime/Animation",
    32: "Action/Adventure",
    33: "Classics",
    34: "Comedy",
    35: "Documentary",
    36: "Drama",
    37: "Family",
    38: "Foreign",
    39: "Horror",
    40: "Sci-Fi/Fantasy",
    41: "Thriller",
    42: "Shorts",
    43: "Shows",
    44: "Trailers"
}

tags = [
    "tag_spotify", "tag_дмитрий", "tag_майнкрафт", "tag_premier", "tag_discord", "tag_other", "tag_show", "tag_auto", 
    "tag_2021", "tag_epidemic", "tag_анимация", "tag_вконтакте", "tag_ferrari", "tag_instagram", "tag_война", 
    "tag_юмор", "tag_what", "tag_humour", "tag_путин", "tag_links", "tag_animal", "tag_episode", "tag_join", 
    "tag_путина", "tag_news", "tag_song", "tag_director", "tag_sports", "tag_mercedes", "tag_final", "tag_сериал", 
    "tag_если", "tag_авто", "tag_videos", "tag_новости", "tag_porsche", "tag_football", "tag_пожалуйста", "tag_телега", 
    "tag_more", "tag_puppy", "tag_есть", "tag_this", "tag_official", "tag_free", "tag_twitter", "tag_code", "tag_your", 
    "tag_группа", "tag_россии", "tag_para", "tag_vlog", "tag_link", "tag_family", "tag_animation", "tag_from", "tag_маразм", 
    "tag_über", "tag_dans", "tag_pets", "tag_will", "tag_twitch", "tag_game", "tag_iphone", "tag_sport", "tag_world", 
    "tag_time", "tag_with", "tag_highlights", "tag_обзор", "tag_here", "tag_latest", "tag_shorts", "tag_сайт", "tag_turbo", 
    "tag_lyrics", "tag_plus", "tag_film", "tag_tuning", "tag_дмитрий потапенко", "tag_support", "tag_audi", "tag_tiktok", 
    "tag_потапенко", "tag_канал", "tag_production", "tag_amazon", "tag_фильмы", "tag_apple", "tag_life", "tag_vidéo", 
    "tag_channel", "tag_have", "tag_которые", "tag_travel", "tag_league", "tag_россия", "tag_science", "tag_tech", 
    "tag_social", "tag_love", "tag_pour", "tag_видео", "tag_album", "tag_make", "tag_sony", "tag_gameplay", "tag_oficial", 
    "tag_producer", "tag_vlogs", "tag_фильм", "tag_champions", "tag_first", "tag_vous", "tag_trailer", "tag_telegram", 
    "tag_that", "tag_music", "tag_ford", "tag_youtube", "tag_животных", "tag_funny", "tag_кино", "tag_subscribe", 
    "tag_email", "tag_gaming", "tag_comedy", "tag_affiliate", "tag_watch", "tag_like", "tag_minecraft", "tag_about", 
    "tag_facebook", "tag_animals", "tag_movie", "tag_dogs", "tag_follow", "tag_будет", "tag_собака", "tag_меня", 
    "tag_unboxing", "tag_video", "tag_soccer", "tag_cars", "tag_политика", "tag_украина", "tag_live", "tag_click"
]

all_tags = set([i[4:] for i in tags])

categories_id_map = {category_mapping[catid]: catid for catid in category_mapping}
categories = list(categories_id_map.keys())

regions = ['US', 'IN', 'RU', 'FR', 'DE', 'BR', 'JP', 'MX', 'KR', 'GB', 'CA']

# UI Elements
# Category Dropdown
ttk.Label(root, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
category_dropdown = ttk.OptionMenu(root, category_var, categories[0], *categories)
category_dropdown.grid(row=0, column=1, padx=10, pady=5)

# Title Entry
ttk.Label(root, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
title_entry = ttk.Entry(root, textvariable=title_var)
title_entry.grid(row=1, column=1, padx=10, pady=5)

# Description Entry
ttk.Label(root, text="Description:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
description_entry = ttk.Entry(root, textvariable=description_var)
description_entry.grid(row=2, column=1, padx=10, pady=5)

# Tags Entry
ttk.Label(root, text="Tags:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
tags_entry = ttk.Entry(root, textvariable=tags_var)
tags_entry.grid(row=3, column=1, padx=10, pady=5)

# Comments Disabled Checkbox
ttk.Label(root, text="Comments Disabled:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
comments_checkbox = ttk.Checkbutton(root, variable=comments_disabled_var)
comments_checkbox.grid(row=4, column=1, padx=10, pady=5)

# Region Dropdown
ttk.Label(root, text="Region:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
region_dropdown = ttk.OptionMenu(root, region_var, regions[0], *regions)
region_dropdown.grid(row=5, column=1, padx=10, pady=5)

# Duration Entry
ttk.Label(root, text="Duration (seconds):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
duration_entry = ttk.Entry(root, textvariable=duration_var)
duration_entry.grid(row=6, column=1, padx=10, pady=5)

# Definition Dropdown
ttk.Label(root, text="Definition:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
definition_dropdown = ttk.OptionMenu(root, definition_var, "HD", "HD", "SD")
definition_dropdown.grid(row=7, column=1, padx=10, pady=5)

# Caption Checkbox
ttk.Label(root, text="Caption:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
caption_checkbox = ttk.Checkbutton(root, variable=caption_var)
caption_checkbox.grid(row=8, column=1, padx=10, pady=5)

# Comment Sentiment Slider
ttk.Label(root, text="Comment Sentiment:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
# sentiment_slider = ttk.Scale(root, from_=-1, to=1, orient="horizontal", variable=sentiment_var)
sentiment_value = ttk.Entry(root, textvariable=sentiment_var)
# sentiment_slider.grid(row=9, column=1, padx=10, pady=5)
sentiment_value.grid(row=9, column=1, padx=10, pady=5)
sentiment_value.config(width=5, validate="key", validatecommand=(root.register(lambda P: P.isdigit() or P == '' or (P.count('.') == 1 and len(P.split('.')[-1]) <= 2)), '%P'))

# Subscribers Entry
ttk.Label(root, text="Subscribers:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
subscribers_entry = ttk.Entry(root, textvariable=subscribers_var)
subscribers_entry.grid(row=10, column=1, padx=10, pady=5)

# Submit Button
submit_button = ttk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=11, column=0, columnspan=2, pady=20)

generated_tags_label = ttk.Label(root, text="", wraplength=400)
generated_tags_label.grid(row=12, column=0, padx=10, pady=5, sticky="w", columnspan=2)
predicted_subscribers_label = ttk.Label(root, text="", wraplength=400)
predicted_subscribers_label.grid(row=13, column=0, padx=10, pady=5, sticky="w", columnspan=2)

# Start the application
root.mainloop()