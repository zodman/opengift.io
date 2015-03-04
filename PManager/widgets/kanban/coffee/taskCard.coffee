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

	getStorageKey: ->
		"project_#{@widget.kbnId}task_#{@id}"
	store: ->
		value = @position
		value.status = @status
		@storage(@getStorageKey(), value)
	restore: ->
		value = @storage(@getStorageKey())
		if value? and value.status?
			if @widget.validBox(@)
				@setPosition(value)
				return 
		do @setPosition
		do @store
	startMove: ->
		@position = do @el.position
	completeMove: ->
		@position = do @el.position
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
	setPosition:(position) ->
		if not position?
			position = do @getPositionDefault
		currentOffset = @widget.offset
		position = {
			left: position.left
			top: position.top
		}
		@el.animate(position, 0)
		@position = do @el.position
	initialize: ->
		do @restore
		do @update
		do @render

