class KanbanBox
	constructor: (@el) ->
		do @update
	getBoundaries: ->
		if not @el.offset()?
			return
		offset = do @el.offset
		{	
			left: offset.left
			top: offset.top
			right: offset.left + do @el.width
			bottom: offset.top + do @el.height
		} if @el
	update: ->
		@container = do @getBoundaries
	setOffset:(offset) ->
		@el.offset offset
		do @update
	getOffset: ->
		{ left: @container.left, top: @container.top }
	insideOf:(kanbanBox) ->
		if not kanbanBox? then return false
		if @container.left < kanbanBox.left then return false
		if @container.right > kanbanBox.right then return false
		if @container.top < kanbanBox.top then return false
		if @container.bottom > kanbanBox.bottom then return false
		true