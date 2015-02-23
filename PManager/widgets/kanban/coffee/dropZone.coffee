class DropZone extends KanbanBox
	constructor: (options) ->
		return false unless options.el?
		super options.el 
		@projectRow = options.projectRow
		@nextOffset = { left: 0, top: 0 }
		@step = @projectRow.dropDefaultLayout
	getNextOffset:(kanbanBox) -> 
		do addNextOffset
		maxWidth = @container.right - @container.left -
			kanbanBox.container.right + kanbanBox.container.left
		return {
			left: @container.left - kanbanBox.container.left +
				@nextOffset.left % maxWidth
			top: @container.top - kanbanBox.container.top +
				@nextOffset.top
		}
	addNextOffset: ->
		@nextOffset = {
			top: @nextOffset.top + @step.top
			left: @nextOffset.left + @step.left
		}
	resize:(height) ->
		if height? 
			@el.css('height', height + 'px')
			do @update