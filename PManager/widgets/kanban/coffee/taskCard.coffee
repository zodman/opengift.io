class TaskCard extends KanbanBox
	constructor:(options) ->
		super options.el
		@projectRow = options.projectRow
		@model = options.model || {}
		@el = options.el
		@view = options.view || {}
		@dropZones = options.dropZones
		@view.render = @render
		do @view.render
	render: =>
		$(@el).show()
	getStoreKey: ->
		"#{@projectRow.storageKeyPrefix}tsk_#{@model.get('id')}"
	store: ->
		value = do @getOffset
		value.status = @model.get 'status'
		value = JSON.stringify value
		window.localStorage.setItem(do @getStoreKey, value)
	restore: ->
		value = window.localStorage.getItem(do @getStoreKey)
		zone = @dropZones[@model.get('status')]
		if value?
			value = JSON.parse(value)
			if @insideOf(zone)
				@setOffset(value)
			else
				@setOffset(zone)
		else
			@setOffset(zone)
	move: (destination, fn) ->
		moveProp = {
			left: "-"
			top: "-"
		}
		leftMv = @container.left - destination.left
		if leftMv < 0
			moveProp.left = "+"
			leftMv *= -1
		moveProp.left += "=#{leftMv}px"
		topMv = @container.top - destination.top
		if topMv < 0
			moveProp.top = "+"
			topMv *= -1
		moveProp.top += "=#{topMv}px" 
		@el.animate(moveProp, MOVE_TIME, ->
			fn.call @el
			do @update
			do @store
		)