# main file which starts up kanban draw board
class Kanban
	@browser_is_supported: ->
	    if window.navigator.appName == "Microsoft Internet Explorer"
	      return document.documentMode >= 8
	    if /iP(od|hone)/i.test(window.navigator.userAgent)
	      return false
	    if /Android/i.test(window.navigator.userAgent)
	      return false if /Mobile/i.test(window.navigator.userAgent)
	    return true
    constructor: (@projectRow, @options) ->
    	@setDefaultValues()
    	@setup()
	setup: ->
		@tasksSelector = @options.tasksSelector if @options.tasksSelector?
		@dropZoneSelector = @options.dropZoneSelector if @options.dropZoneSelector?
		do @loadTasks
		do @loadZones
		@drawBoard = new DrawBoard({
			el: @projectRow
			tasks: @tasks
			dropZones: @dropZones
		})

	setDefaultValues: ->
		@projectRow = $ @projectRow
		@tasksSelector = '.js-task-wrapper'
		@tasks = []
		@drawBoard = {}
		@dropZoneSelector = '.js-tasks-column'
		@dropZones = []
		@storageKeyPrefix = 'hl_kb_'
		@animationTime = 200
		@dropDefaultLayout = { left: 20, top: 20 }
	loadTasks: ->
		@projectRow.find(@tasksSelector).each((index, el) =>
			@tasks.push(new TaskCard({
				el: $(el)
				projectRow: @
			}))
		)
	loadZones: ->
		@projectRow.find(@dropZoneSelector).each((index, el) =>
			@dropZones.push(new DropZone({
				el:$(el)
				projectRow: @
			}))
		)



$ = jQuery

$.fn.extend({
	kanban: (options) ->
		return this unless Kanban.browser_is_supported()
		this.each (projectRow) ->
			$this = $ this
			kanban = $this.data('kanban')
			if options is 'destroy' && kanban instanceof Kanban
				kanban.destroy()
			else unless kanban instanceof Kanban
				$this.data('kanban', new Kanban(this, options))
		return		
})
$(document).ready(-> 
	$('.js-project-row').kanban({test:'test'})
)