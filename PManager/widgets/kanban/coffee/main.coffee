# main file which starts up kanban draw board

(( $ ) ->
	$.widget('tonakai.kanban', {
		options: {
			animationTime: 200
			storagePrefix: 'hl_kb_'
			defaultStep: { left: 40, top: 40 }
			drops: '.js-tasks-column'
			tasks: '.js-task-wrapper'
			attributeName: 'rel'
			resizable: {minHeight: 400}
		},
		getDropByPosition: (position) ->
			for key, drop of @dropAreas
				if drop.position.left + drop.borders.left < position.left and drop.position.left + drop.width - drop.borders.right > position.left
					return drop
			return false
		validBox: (position, task) ->
			drop = @dropAreas[task.status]
			return false unless drop?
			boundaries = {
				left: drop.position.left + drop.borders.left
				right: drop.position.left + drop.width - drop.borders.right
			}
			if position.left < boundaries.left
				return false
			if position.left > boundaries.right
				return false
			if position.left + task.el.width() > boundaries.right
				return false
			return true
		onStatusChange: (task) ->
			@_trigger(':onstatuschange', @, task)
		onDrop: (task, drop) ->
			@_trigger(':ondrop', @, { drop: drop, task: task})
		onDragRevert:(task) ->
			@_trigger(':dragrevert', @, task)
		onDragStart:(task) ->
			@_trigger(':dragstart', @, task)
		onDragEnd:(task) ->
			@_trigger(':dragend', @, task)
		_storeHeight: (height) ->
			window.localStorage.setItem(@_storeResizeKey(), height)
		_restoreHeight: ->
			val = window.localStorage.getItem(@_storeResizeKey())
			return @options.resizable.minHeight unless val?
			try
				val = JSON.parse(val)
				return val
			catch e
				return @options.resizable.minHeight
		getTask:(element) ->
			id = element.attr(@options.attributeName)
			return @tasks[id] if @tasks[id]
			return false
		_create: ->
			return false unless @_browser_is_supported()
			return false unless @_dependencies_resolved()
			@kbnId = @element.attr(@options.attributeName)
			@dropAreas = {}
			@tasks = {}
			@scope = "project_kanban_#{@kbnId}"
			@offset = do @element.offset
			do @_setup
		_setOption: (key, value) ->
			@options[ key ] = value
			@_super( key, value );
			do @update
		_setup: ->
			do @_initDrops
			do @_initTasks
			do @_initResizable
			@_trigger(':ready', @)
		setHeight:(height) ->
			@element.css('height', height + 'px')
			for drop of @drops
				drop.setHeight(height)
			@_storeHeight(height)
		getHeight:->
			return @element.height()
		_initResizable: ->
			@element.resizable({
				handles: "s"
				minHeight: 400
				create: =>
					height = do @_restoreHeight
					@setHeight(height)
				stop: =>
					height = @element.height()
					for drop of @drops
						drop.setHeight(height)
					@_storeHeight(height)
			})
		isDroppable:(droppable) ->

			if droppable.hasClass?(@options.drops.slice(1))
				return true
			return false
		_storeResizeKey: ->
			"#{@storagePrefix}project_#{@knbId}"
		_initDrops: ->
			@element.find(@options.drops).each((index, el) =>
				$el = $ el
				@addDrop($el)
			)
		_initTasks: ->
			@element.find(@options.tasks).each((index, el) =>
				$el = $ el
				@addTask($el)
			)
		update: ->
			do @render
		addDrop:($el) ->
			@dropAreas[$el.attr(@options.attributeName)] = new DropArea($el, @)			
			@_trigger(':dropadd', @, @dropAreas[$el.attr(@options.attributeName)])
		addTask:($el) ->
			task = new Task($el, @)
			@tasks[$el.attr(@options.attributeName)] = task
			@_trigger(':taskadd', @, @tasks[$el.attr(@options.attributeName)])
			do task.initialize			
		render: ->
			for key,task of @tasks
				do task.render
			return
		_browser_is_supported: ->
			if window.navigator.appName == "Microsoft Internet Explorer"
				return document.documentMode >= 8
			if /iP(od|hone)/i.test(window.navigator.userAgent)
				return false
			if /Android/i.test(window.navigator.userAgent)
				return false if /Mobile/i.test(window.navigator.userAgent)
			return true
		_dependencies_resolved: ->
			return false unless $().draggable?
			return false unless $().droppable?
			return true
	})
)( jQuery )


