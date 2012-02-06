set the source_directory to choose folder "Select the folder containing senior information"
tell the application "Finder"
	set the text_files to every file in source_directory whose name starts with "page"
	set the image_files to every file in source_directory whose name starts with "images"
end tell

tell the app "Adobe InDesign CS5"
repeat with pageNum from 1 to (the count of text_files)
	
end repeat
end