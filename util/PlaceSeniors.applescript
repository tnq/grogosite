set the source_directory to choose folder "Select the folder containing senior information"
tell the application "Finder"
	set the text_files to (every file in source_directory whose name starts with "page") as alias list
	set the image_files to (every file in source_directory whose name starts with "images") as alias list
end tell

to getPageItem(pageNum, scriptLabel)
	tell application "Adobe InDesign CS5"
		tell the active document
			set overriddenItems to every page item of page pageNum whose label is scriptLabel
			if the length of overriddenItems is greater than or equal to 1 then
				return item 1 of overriddenItems
			else
				repeat with i in master page items of page pageNum
					if the label of i is scriptLabel then
						return override i destination page page pageNum
					end if
				end repeat
			end if
		end tell
	end tell
end getPageItem

tell the application "Adobe InDesign CS5"
	tell the active document
		repeat with pageNum from 1 to (the count of text_files)
			repeat while pageNum is greater than (the count of every page)
				make new spread at after the last spread with properties {applied master:master spread "8-8x8"}
			end repeat
			set the textBoxGroup to my getPageItem(pageNum, "text")
			tell the parent story of text frame 1 of textBoxGroup
				set the contents to ""
				tell insertion point -1
					place (item pageNum of text_files)
				end tell
			end tell
		end repeat
	end tell
end tell