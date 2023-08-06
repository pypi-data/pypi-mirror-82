def bokeh_matplot(df, i_col, j_col, data_col, data_range=None, n_colors=21,
                  label_ticks=True, colormap='RdBu_r', plot_width=1000,
                  plot_height=1000, x_axis_location='auto',
                  toolbar_location='left',
                  tools='reset,resize,hover,save,pan,box_zoom,wheel_zoom',
                  **kwargs):
    """
    Create Bokeh plot of a matrix.

    Parameters
    ----------
    df : Pandas DataFrame
        Tidy DataFrame to be plotted as a matrix.
    i_col : hashable object
        Column in `df` to be used for row indices of matrix.
    j_col : hashable object
        Column in `df` to be used for column indices of matrix.
    data_col : hashable object
        Column containing values to be plotted.  These values
        set which color is displayed in the plot and also are
        displayed in the hover tool.
    data_range : array_like, shape (2,)
        Low and high values that data may take, used for scaling
        the color.  Default is the range of the inputted data.
    n_colors : int, default = 21
        Number of colors to be used in colormap.
    label_ticks : bool, default = True
        If False, do not put tick labels
    colormap : str, default = 'RdBu_r'
        Any of the allowed seaborn colormaps.
    plot_width : int, default 1000
        Width of plot in pixels.
    plot_height : int, default 1000
        Height of plot in pixels.
    x_axis_location : str, default = None
        Location of the x-axis around the plot. If 'auto' and first
        element of `df[i_col]` is numerical, x-axis will be placed below
        with the lower left corner as the origin. Otherwise, above
        with the upper left corner as the origin.
    toolbar_location : str, default = 'left'
        Location of the Bokeh toolbar around the plot
    tools : str, default = 'reset,resize,hover,save,pan,box_zoom,wheel_zoom'
        Tools to show in the Bokeh toolbar
    **kwargs
        Arbitrary keyword arguments passed to bokeh.plotting.figure

    Returns
    -------
    Bokeh plotting object


    Examples
    --------
    >>> a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> data = np.array(np.unravel_index(range(9), a.shape) + (a.ravel(),)).T
    >>> df = pd.DataFrame(data, columns=['i', 'j', 'data'])
    >>> bokeh.plotting.output_file('test_matplot.html')
    >>> p = bokeh_matplot(df, i_col, j_col, data_col, n_colors=21,
                          colormap='RdBu_r', plot_width=1000,
                          plot_height=1000)
    >>> bokeh.plotting.show(p)
    """
    # Copy the DataFrame
    df_ = df.copy()

    # Convert i, j to strings so not interpreted as physical space
    df_[i_col] = df_[i_col].astype(str)
    df_[j_col] = df_[j_col].astype(str)

    # Get data range
    if data_range is None:
        data_range = (df[data_col].min(), df[data_col].max())
    elif (data_range[0] > df[data_col].min()) \
            or (data_range[1] < df[data_col].max()):
        raise RuntimeError('Data out of specified range.')

    # Get colors
    palette = sns.color_palette(colormap, n_colors)

    # Compute colors for squares
    df_['color'] = df_[data_col].apply(data_to_hex_color,
                                       args=(palette, data_range))

    # Data source
    source = bokeh.plotting.ColumnDataSource(df_)

    # only reverse the y-axis and put the x-axis on top
    # if the x-axis is categorical:
    if x_axis_location == 'auto':
        if isinstance(df[j_col].iloc[0], numbers.Number):
            y_range = list(df_[i_col].unique())
            x_axis_location = 'below'
        else:
            y_range = list(reversed(list(df_[i_col].unique())))
            x_axis_location = 'above'
    elif x_axis_location == 'above':
        y_range = list(reversed(list(df_[i_col].unique())))
    elif x_axis_location == 'below':
        y_range = list(df_[i_col].unique())

    # Set up figure
    p = bokeh.plotting.figure(x_range=list(df_[j_col].unique()),
                              y_range=y_range,
                              x_axis_location=x_axis_location,
                              plot_width=plot_width,
                              plot_height=plot_height,
                              toolbar_location=toolbar_location,
                              tools=tools, **kwargs)

    # Populate colored squares
    p.rect(j_col, i_col, 1, 1, source=source, color='color', line_color=None)

    # Set remaining properties
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    if label_ticks:
        p.axis.major_label_text_font_size = '8pt'
    else:
        p.axis.major_label_text_color = None
        p.axis.major_label_text_font_size = '0pt'
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = np.pi / 3

    # Build hover tool
    hover = p.select(dict(type=bokeh.models.HoverTool))
    hover.tooltips = collections.OrderedDict([('i', '  @' + i_col),
                                              ('j', '  @' + j_col),
                                              (data_col, '  @' + data_col)])

    return p


def bokeh_boxplot(df, value, label, ylabel=None, sort=True, plot_width=650,
                  plot_height=450, box_fill_color='medium_purple',
                  background_fill_color='#DFDFE5',
                  tools='reset,resize,hover,save,pan,box_zoom,wheel_zoom',
                  **kwargs):
    """
    Make a Bokeh box plot from a tidy DataFrame.

    Parameters
    ----------
    df : tidy Pandas DataFrame
        DataFrame to be used for plotting
    value : hashable object
        Column of DataFrame containing data to be used.
    label : hashable object
        Column of DataFrame use to categorize.
    ylabel : str, default None
        Text for y-axis label
    sort : Boolean, default True
        If True, sort DataFrame by label so that x-axis labels are
        alphabetical.
    plot_width : int, default 650
        Width of plot in pixels.
    plot_height : int, default 450
        Height of plot in pixels.
    box_fill_color : string
        Fill color of boxes, default = 'medium_purple'
    background_fill_color : str, default = '#DFDFE5'
        Fill color of the plot background
    tools : str, default = 'reset,resize,hover,save,pan,box_zoom,wheel_zoom'
        Tools to show in the Bokeh toolbar
    **kwargs
        Arbitrary keyword arguments passed to bokeh.plotting.figure

    Returns
    -------
    Bokeh plotting object

    Example
    -------
    >>> cats = list('ABCD')
    >>> values = np.random.randn(200)
    >>> labels = np.random.choice(cats, 200)
    >>> df = pd.DataFrame({'label': labels, 'value': values})
    >>> bokeh.plotting.output_file('test_boxplot.html')
    >>> p = bokeh_boxplot(df, value='value', label='label')
    >>> bokeh.plotting.show(p)

    Notes
    -----
    .. Based largely on example code found here:
     https://github.com/bokeh/bokeh/blob/master/examples/plotting/file/boxplot.py
    """

    # Sort DataFrame by labels for alphabetical x-labeling
    if sort:
        df_sort = df.sort_values(label)
    else:
        df_sort = df.copy()

    # Convert labels to string to allow categorical axis labels
    df_sort[label] = df_sort[label].astype(str)

    # Get the categories
    cats = list(df_sort[label].unique())

    # Group Data frame
    df_gb = df_sort.groupby(label)

    # Compute quartiles for each group
    q1 = df_gb[value].quantile(q=0.25)
    q2 = df_gb[value].quantile(q=0.5)
    q3 = df_gb[value].quantile(q=0.75)

    # Compute interquartile region and upper and lower bounds for outliers
    iqr = q3 - q1
    upper_cutoff = q3 + 1.5 * iqr
    lower_cutoff = q1 - 1.5 * iqr

    # Find the outliers for each category
    def outliers(group):
        cat = group.name
        outlier_inds = (group[value] > upper_cutoff[cat]) | \
                       (group[value] < lower_cutoff[cat])
        return group[value][outlier_inds]

    # Apply outlier finder
    out = df_gb.apply(outliers).dropna()

    # Points of outliers for plotting
    outx = []
    outy = []
    if not out.empty:
        for cat in cats:
            if not out[cat].empty:
                for val in out[cat]:
                    outx.append(cat)
                    outy.append(val)

    # Shrink whiskers to smallest and largest non-outlier
    qmin = df_gb[value].min()
    qmax = df_gb[value].max()
    upper = upper_cutoff.combine(qmax, min)
    lower = lower_cutoff.combine(qmin, max)

    # Reindex to make sure ordering is right when plotting
    upper = upper.reindex(cats)
    lower = lower.reindex(cats)
    q1 = q1.reindex(cats)
    q2 = q2.reindex(cats)
    q3 = q3.reindex(cats)

    # Build figure
    p = bokeh.plotting.figure(x_range=cats,
                              background_fill_color=background_fill_color,
                              plot_width=plot_width, plot_height=plot_height,
                              tools=tools,
                              **kwargs)
    p.ygrid.grid_line_color = 'white'
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_width = 2
    p.yaxis.axis_label = ylabel

    # stems
    p.segment(cats, upper, cats, q3, line_width=2, line_color="black")
    p.segment(cats, lower, cats, q1, line_width=2, line_color="black")

    # boxes
    p.rect(cats, (q3 + q1) / 2, 0.5, q3 - q1, fill_color="mediumpurple",
           alpha=0.7, line_width=2, line_color="black")

    # median (almost-0 height rects simpler than segments)
    y_range = qmax.max() - qmin.min()
    p.rect(cats, q2, 0.5, 0.0001 * y_range, line_color="black",
           line_width=2, fill_color='black')

    # whiskers (almost-0 height rects simpler than segments with
    # categorial x-axis)
    p.rect(cats, lower, 0.2, 0.0001 * y_range, line_color='black',
           fill_color='black')
    p.rect(cats, upper, 0.2, 0.0001 * y_range, line_color='black',
           fill_color='black')

    # outliers
    p.circle(outx, outy, size=6, color='black')

    return p


def bokeh_imrgb(im, plot_height=400, plot_width=None,
                tools='pan,box_zoom,wheel_zoom,reset,resize'):
    """
    Make a Bokeh Figure instance displaying an RGB image.
    If the image is already 32 bit, just display it
    """
    # Make 32 bit image
    if len(im.shape) == 2 and im.dtype == np.uint32:
        im_disp = im
    else:
        im_disp = rgb_to_rgba32(im)

    # Get shape
    n, m = im_disp.shape

    # Determine plot height and width
    if plot_height is not None and plot_width is None:
        plot_width = int(m/n * plot_height)
    elif plot_height is None and plot_width is not None:
        plot_height = int(n/m * plot_width)
    elif plot_height is None and plot_width is None:
        plot_heigt = 400
        plot_width = int(m/n * plot_height)

    # Set up figure with appropriate dimensions
    p = bokeh.plotting.figure(plot_height=plot_height, plot_width=plot_width,
                              x_range=[0, m], y_range=[0, n], tools=tools)

    # Display the image, setting the origin and heights/widths properly
    p.image_rgba(image=[im_disp], x=0, y=0, dw=m, dh=n)

    return p


def bokeh_im(im, plot_height=400, plot_width=None,
             color_palette=bokeh.palettes.gray(256),
             tools='pan,box_zoom,wheel_zoom,reset,resize'):
    """
    """
    # Get shape
    n, m = im.shape

    # Determine plot height and width
    if plot_height is not None and plot_width is None:
        plot_width = int(m/n * plot_height)
    elif plot_height is None and plot_width is not None:
        plot_height = int(n/m * plot_width)
    elif plot_height is None and plot_width is None:
        plot_heigt = 400
        plot_width = int(m/n * plot_height)

    p = bokeh.plotting.figure(plot_height=plot_height, plot_width=plot_width,
                              x_range=[0, m], y_range=[0, n], tools=tools)

    # Set color mapper
    color = bokeh.models.LinearColorMapper(color_palette)

    # Display the image
    p.image(image=[im], x=0, y=0, dw=m, dh=n, color_mapper=color)

    return p


def distribution_plot_app(
    x_min=None,
    x_max=None,
    scipy_dist=None,
    transform=None,
    custom_pdf=None,
    custom_pmf=None,
    custom_cdf=None,
    params=None,
    n=400,
    plot_height=200,
    plot_width=300,
    x_axis_label="x",
    title=None,
):
    """
    Build interactive Bokeh app displaying a univariate
    probability distribution.

    Parameters
    ----------
    x_min : float
        Minimum value that the random variable can take in plots.
    x_max : float
        Maximum value that the random variable can take in plots.
    scipy_dist : scipy.stats distribution
        Distribution to use in plotting.
    transform : function or None (default)
        A function of call signature `transform(*params)` that takes
        a tuple or Numpy array of parameters and returns a tuple of
        the same length with transformed parameters.
    custom_pdf : function
        Function with call signature f(x, *params) that computes the
        PDF of a distribution.
    custom_pmf : function
        Function with call signature f(x, *params) that computes the
        PDF of a distribution.
    custom_cdf : function
        Function with call signature F(x, *params) that computes the
        CDF of a distribution.
    params : list of dicts
        A list of parameter specifications. Each entry in the list gives
        specifications for a parameter of the distribution stored as a
        dictionary. Each dictionary must have the following keys.
            name : str, name of the parameter
            start : float, starting point of slider for parameter (the
                smallest allowed value of the parameter)
            end : float, ending point of slider for parameter (the
                largest allowed value of the parameter)
            value : float, the value of the parameter that the slider
                takes initially. Must be between start and end.
            step : float, the step size for the slider
    n : int, default 400
        Number of points to use in making plots of PDF and CDF for
        continuous distributions. This should be large enough to give
        smooth plots.
    plot_height : int, default 200
        Height of plots.
    plot_width : int, default 300
        Width of plots.
    x_axis_label : str, default 'x'
        Label for x-axis.
    title : str, default None
        Title to be displayed above the PDF or PMF plot.

    Returns
    -------
    output : Bokeh app
        An app to visualize the PDF/PMF and CDF. It can be displayed
        with bokeh.io.show(). If it is displayed in a notebook, the
        notebook_url kwarg should be specified.
    """
    if None in [x_min, x_max]:
        raise RuntimeError("`x_min` and `x_max` must be specified.")

    if scipy_dist is None:
        fun_c = custom_cdf
        if (custom_pdf is None and custom_pmf is None) or custom_cdf is None:
            raise RuntimeError(
                "For custom distributions, both PDF/PMF and" + " CDF must be specified."
            )
        if custom_pdf is not None and custom_pmf is not None:
            raise RuntimeError("Can only specify custom PMF or PDF.")
        if custom_pmf is None:
            discrete = False
            fun_p = custom_pdf
        else:
            discrete = True
            fun_p = custom_pmf
    elif custom_pdf is not None or custom_pmf is not None or custom_cdf is not None:
        raise RuntimeError("Can only specify either custom or scipy distribution.")
    else:
        fun_c = scipy_dist.cdf
        if hasattr(scipy_dist, "pmf"):
            discrete = True
            fun_p = scipy_dist.pmf
        else:
            discrete = False
            fun_p = scipy_dist.pdf

    if discrete:
        p_y_axis_label = "PMF"
    else:
        p_y_axis_label = "PDF"

    if params is None:
        raise RuntimeError("`params` must be specified.")

    def _plot_app(doc):
        p_p = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label=p_y_axis_label,
            title=title,
        )
        p_c = bokeh.plotting.figure(
            plot_height=plot_height,
            plot_width=plot_width,
            x_axis_label=x_axis_label,
            y_axis_label="CDF",
        )

        # Link the axes
        p_c.x_range = p_p.x_range

        # Make sure CDF y_range is zero to one
        p_c.y_range = bokeh.models.Range1d(-0.05, 1.05)

        # Make array of parameter values
        param_vals = np.array([param["value"] for param in params])
        if transform is not None:
            param_vals = transform(*param_vals)

        # Set up data for plot
        if discrete:
            x = np.arange(int(np.ceil(x_min)), int(np.floor(x_max)) + 1)
            x_size = x[-1] - x[0]
            x_c = np.empty(2 * len(x))
            x_c[::2] = x
            x_c[1::2] = x
            x_c = np.concatenate(
                (
                    (max(x[0] - 0.05 * x_size, x[0] - 0.95),),
                    x_c,
                    (min(x[-1] + 0.05 * x_size, x[-1] + 0.95),),
                )
            )
            x_cdf = np.concatenate(((x_c[0],), x))
        else:
            x = np.linspace(x_min, x_max, n)
            x_c = x_cdf = x

        # Compute PDF and CDF
        y_p = fun_p(x, *param_vals)
        y_c = fun_c(x_cdf, *param_vals)
        if discrete:
            y_c_plot = np.empty_like(x_c)
            y_c_plot[::2] = y_c
            y_c_plot[1::2] = y_c
            y_c = y_c_plot

        # Set up data sources
        source_p = bokeh.models.ColumnDataSource(data={"x": x, "y_p": y_p})
        source_c = bokeh.models.ColumnDataSource(data={"x": x_c, "y_c": y_c})

        # Plot PDF and CDF
        p_c.line("x", "y_c", source=source_c, line_width=2)
        if discrete:
            p_p.circle("x", "y_p", source=source_p, size=5)
            p_p.segment(x0="x", x1="x", y0=0, y1="y_p", source=source_p, line_width=2)
        else:
            p_p.line("x", "y_p", source=source_p, line_width=2)

        def _callback(attr, old, new):
            param_vals = tuple([slider.value for slider in sliders])
            if transform is not None:
                param_vals = transform(*param_vals)

            # Compute PDF and CDF
            source_p.data["y_p"] = fun_p(x, *param_vals)
            y_c = fun_c(x_cdf, *param_vals)
            if discrete:
                y_c_plot = np.empty_like(x_c)
                y_c_plot[::2] = y_c
                y_c_plot[1::2] = y_c
                y_c = y_c_plot
            source_c.data["y_c"] = y_c

        sliders = [
            bokeh.models.Slider(
                start=param["start"],
                end=param["end"],
                value=param["value"],
                step=param["step"],
                title=param["name"],
            )
            for param in params
        ]
        for slider in sliders:
            slider.on_change("value", _callback)

        # Add the plot to the app
        widgets = bokeh.layouts.widgetbox(sliders)
        grid = bokeh.layouts.gridplot([p_p, p_c], ncols=2)
        doc.add_root(bokeh.layouts.column(widgets, grid))

    handler = bokeh.application.handlers.FunctionHandler(_plot_app)
    return bokeh.application.Application(handler)


def adjust_range(element, buffer=0.05):
    """
    Adjust soft ranges of dimensions of HoloViews element.

    Parameters
    ----------
    element : holoviews element
        Element which will have the `soft_range` of each kdim and vdim
        recomputed to give a buffer around the glyphs.
    buffer : float, default 0.05
        Buffer, as a fraction of the whole data range, to give around
        data.

    Returns
    -------
    output : holoviews element
        Inputted HoloViews element with updated soft_ranges for its
        dimensions.
    """
    # This only works with DataFrames
    if type(element.data) != pd.core.frame.DataFrame:
        raise RuntimeError("Can only adjust range if data is Pandas DataFrame.")

    # Adjust ranges of kdims
    for i, dim in enumerate(element.kdims):
        if element.data[dim.name].dtype in [float, int]:
            data_range = (element.data[dim.name].min(), element.data[dim.name].max())
            if data_range[1] - data_range[0] > 0:
                buff = buffer * (data_range[1] - data_range[0])
                element.kdims[i].soft_range = (
                    data_range[0] - buff,
                    data_range[1] + buff,
                )

    # Adjust ranges of vdims
    for i, dim in enumerate(element.vdims):
        if element.data[dim.name].dtype in [float, int]:
            data_range = (element.data[dim.name].min(), element.data[dim.name].max())
            if data_range[1] - data_range[0] > 0:
                buff = buffer * (data_range[1] - data_range[0])
                element.vdims[i].soft_range = (
                    data_range[0] - buff,
                    data_range[1] + buff,
                )

    return element

