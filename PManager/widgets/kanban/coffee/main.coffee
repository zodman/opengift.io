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
	@dependencies_resolved: ->
		return false unless $().draggable?
		return false unless $().droppable?
		return true

	constructor: (@projectRow, @options) ->
		do @setDefaultValues
		do @setup
		do @render

	ready: -> 
	filter: ->
		console.log "filter"
	render: ->
		console.log "render called"

	setup: ->
		if @options? and @options.ready?
			@ready = @options.ready

	setDefaultValues: ->
		@OBJECT_READY = 1
		@OBJECT_NOT_READY = 0
		@ANIMATION_TIME = 200
		@STORAGE_PREFIX = 'hl_kb_'
		@DROP_DEFAULT_STEP = { left: 20, top: 20 }

$ = jQuery

$.fn.extend({
	kanban: (options) ->
		return this unless Kanban.browser_is_supported()
		return this unless Kanban.dependencies_resolved()
		this.each (projectRow) ->
			$this = $ this
			kanban = $this.data('kanban')
			if options is 'destroy' && kanban instanceof Kanban
				kanban.destroy()
			else unless kanban instanceof Kanban
				$this.data('kanban', new Kanban(this, options))
		return		
})
