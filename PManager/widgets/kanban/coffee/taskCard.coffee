class Task
	constructor: (@el, @widget) ->
		@position = do @el.position
		@status = false
		@storage = ->
		@id = @el.attr('rel')
		@el.draggable({
			stack: "div"
			distance: 0
			scope: @widget.scope
			containment: "parent"
			create: =>
				@el.css('z-index', DropArea.getIndex())
			start: =>
				do @startMove
				@widget.onDragStart(@)
			revert:(droppable) =>
				@widget.onDragRevert(@)
				return false if @widget.isDroppable(droppable)
				return true
			stop:(event, ui) =>
				@widget.onDragEnd(@)
			})
	render: ->
		@el.show()
	update: ->

	setStatus:(value) ->
		@status = value
		if not @widget.validBox(@position, @)
			@setPosition(null, @widget.options.animationTime)
			do @store

	getStorageKey: ->
		"project_#{@widget.kbnId}task_#{@id}"
	store: ->
		value = @position
		value.status = @status
		@storage(@getStorageKey(), value)
	restore: ->
		value = @storage(@getStorageKey())
		if value? and value.status?
			if @widget.validBox(value, @)
				@setPosition(value)
				return 
		do @setPosition
		do @store
	startMove: ->
		@position = do @el.position
	completeMove: ->
		newPosition = do @el.position
		drop = @.widget.getDropByPosition(newPosition)
		return do @failMove unless drop?
		@position = newPosition
		if drop.status != @status
			@status = drop.status
			@widget.onStatusChange(@)
		do @store
	failMove: ->
		@el.animate(@position, @widget.options.animationTime, =>
			do @store
		)
	getPositionDefault: ->
		drop = @widget.dropAreas[@status]
		elW = do @el.width
		offset = drop.getNextOffset(elW)
		return offset
	setPosition:(position, animateDuration) ->
		if not animateDuration? 
			animateDuration = 0
		if not position?
			position = do @getPositionDefault
		currentOffset = @widget.offset
		position = {
			left: position.left
			top: position.top
		}
		@el.animate(position, animateDuration)
		@position = do @el.position
	initialize: ->
		do @restore
		do @update
		do @render

