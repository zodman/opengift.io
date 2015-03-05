class DropArea
	@count: 2
	@getIndex: ->
		DropArea.count += 1
		return DropArea.count
	constructor: (el, widget) ->
		@el = $ el
		@status = @el.attr(widget.options.attributeName)
		@step = widget.options.defaultStep
		@position = do @el.position
		@borders = do @getBorders
		@nextOffset = { left: 0, top: 0 }
		@width = do @el.width
		@el.droppable({
			tolerance: "fit"
			hoverClass: "highlighted"
			scope: widget.scope
			create: (event, ui) =>
				@el.css('z-index', 1)
			drop:(event, ui) =>
				task = @widget.getTask(ui.draggable)
				@widget.onDrop(task, @)
			accept:(draggable) =>
				return true
		})
		@widget = widget
	getBorders: ->
		return {
			left: (parseInt(@el.css('border-left-width')) +
				parseInt(@el.css('padding-left')) +
				parseInt(@el.css('margin-left')))
			right: (parseInt(@el.css('border-right-width')) +
				parseInt(@el.css('padding-right')) +
				parseInt(@el.css('margin-right')))
			top: (parseInt(@el.css('border-top-width')) +
				parseInt(@el.css('padding-top')) +
				parseInt(@el.css('margin-top')))
			bottom: (parseInt(@el.css('border-bottom-width')) +
				parseInt(@el.css('padding-bottom')) +
				parseInt(@el.css('margin-bottom')))
		}
	getNextOffset:(elementWidth, elementHeight) ->
		widthLimit = @width - elementWidth - @borders.right
		heightLimit = @el.height() - elementHeight
		currentOffset = @nextOffset
		@nextOffset = {
			left: (@nextOffset.left + @step.left) % widthLimit
			top: @nextOffset.top + @step.top
		}
		offs = {
			left: @borders.left + @position.left + currentOffset.left
			top:  @borders.top + currentOffset.top
		}
		if offs.top > heightLimit
			@widget.setHeight(offs.top + elementHeight + @borders.bottom)

		return offs
	setHeight:(height)->
		if not height?
			height = @widget.options.resizable.minHeight || 0	
		@el.css('height', height + 'px')
