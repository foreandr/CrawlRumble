
import hyperSel

def RUMBLE_CHANNEL_SCRAPER(person_name, channel_name, type):
    all_current_content = get_content_as_string(name=person_name)
    # print(all_current_content)
    break_both_loops = False
    posts = []
    start = time.time()
    for i in range(1000):
        
        if break_both_loops:
            break
        url = f"https://rumble.com/{type}/{channel_name}?page={i}"

        if url in all_current_content:
            continue

        response = requests.get(url)
        if response.ok:
            # print(i)
            # Parse the HTML content using Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all div elements that contain the video information
            video_divs = soup.select('article.video-item')
            consequtive_num_dupes = 0
            
            for div in video_divs: # Loop through the video divs and extract the video information
                if consequtive_num_dupes > 5:
                    break_both_loops = True
                    break

                a_tag = div.find('a', {'class': 'video-item--a'})
                href = a_tag['href']
                full_url = 'https://rumble.com/' + href

                temp_title, temp_description, url = get_rumble_details_from_url(link=full_url)
                
                if temp_title == "":
                    continue
                
                title = fix_title(temp_title)

                desc = fix_desc(temp_description)
                desc = desc.replace("\n", " ").replace("\t", " ").replace("\r", " ")
                
                posts.append([title, desc, url, "rumble", person_name])
        else:
            break
    # print(f"DONE [RUMBLE][{person_name}]", time.time() - start)
    db.group_insert(posts)
    colors.logging_print_color(color="light_green", text_to_color="RUMBLE", pre_text=F"DONE [{db.count_all_posts()}][NUM:{len(posts)}]", post_text=F"{person_name} - [{round(time.time() - start, 2)}]")
    # colors.logging_print_color(color="green", text_to_color="REDTUBE", other_text="hello world")

def rumble_upload_full_channels_from_file():
    rumble_posts = get_rumble_names_and_ids_from_file()

    for i in rumble_posts:
        name, channel_name, type = i[0], i[1], i[2]
        # print(name, channel_name, type)
        RUMBLE_CHANNEL_SCRAPER(person_name=name, channel_name=channel_name, type=type)
    # modules.UPDATE_POST_TO_LIVE_BY_ME(1)

def get_rumble_details_from_url(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_section = soup.find('html').find('body').find('main').find('article')
        
        title = main_section.find('h1', {'class': 'h1'}).text

        description_section = soup.find('div', {'class': 'media-description-section'})
        description_text = description_section.find('p', {'class': 'media-description media-description--first'}).text.strip().replace("Show more", "")

        return title, description_text, link
    except:
        return "","",""    

if __name__ == '__main__':
    print("hello world")
