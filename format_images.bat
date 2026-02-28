#!/bin/bash

# 1. Check if there are any new photos to process
if ls _raw_photos/*.{jpg,jpeg,png,JPG,JPEG,PNG} 1> /dev/null 2>&1; then
    echo "Processing new photos..."
    
    # 2. Convert and resize to WebP directly into the Jekyll images folder
    magick mogrify -path assets/images/ -resize "1200x>" -quality 80 -format webp _raw_photos/*.{jpg,jpeg,png,JPG,JPEG,PNG}
    
    # 3. Move the originals to the archive so they aren't processed again
    mv _raw_photos/*.{jpg,jpeg,png,JPG,JPEG,PNG} _raw_photos/archive/
    echo "Photos optimized and originals archived."
else
    echo "No new photos found. Skipping optimization."
fi

# 4. Stage all changes (new post + new images)
git add .

# 5. Commit the changes to Git with the current date/time
git commit -m "New blog post and photos published on $(date +'%Y-%m-%d %H:%M')"

# 6. Push to GitHub Pages to make the site live
git push origin main

echo "Success! Your new post is live."