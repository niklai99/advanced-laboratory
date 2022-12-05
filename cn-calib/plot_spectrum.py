def plot_energy_spectrum(
    x, y,
    fig, 
    energy_filter = None,
    idx           = 1, 
    nrows         = 1, 
    ncols         = 1,
    bins          = 200,
    label         = "",
    ecolor        = "#06416D", 
    fcolor        = "#7eb0d5",
    title         = "Energy Spectrum",
    xlabel        = "Energy [ADC counts]",
    ylabel        = "Counts",
    ax            = None
):    
    if ax is None:
        ax = fig.add_subplot(nrows, ncols, idx)
        
    ax.hist(
        x[energy_filter],
        weights   = y[energy_filter],
        bins      = bins, 
        histtype  = "stepfilled", 
        edgecolor = ecolor, 
        facecolor = fcolor,
        label     = label
    )
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    ax.set_xlim(x[energy_filter].min(), x[energy_filter].max())
    
    return ax

def plot_time_spectrum(
    x, y,
    fig, 
    idx           = 1, 
    nrows         = 1, 
    ncols         = 1,
    bins          = 200,
    label         = "",
    ecolor        = "#06416D", 
    fcolor        = "#7eb0d5",
    title         = "Time Spectrum",
    xlabel        = "Time [ns]",
    ylabel        = "Counts",
    ax            = None
):    
    if ax is None:
        ax = fig.add_subplot(nrows, ncols, idx)
        
    ax.hist(
        x,
        weights   = y,
        bins      = bins, 
        histtype  = "stepfilled", 
        edgecolor = ecolor, 
        facecolor = fcolor,
        label     = label
    )
    
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    ax.set_xlim(x.min(), x.max())
    
    return ax
    