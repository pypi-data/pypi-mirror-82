"""
@file
@brief CorrPlot functionalities.

It comes from `corrplot.py <https://raw.githubusercontent.com/biokit/biokit/master/biokit/viz/corrplot.py>`_
which I copied here because the module does not properly work on Python 3 (import issues).
See also `biokit license <https://github.com/biokit/biokit/blob/master/LICENSE>`_.

:author: Thomas Cokelaer
:references: http://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html
"""
import numpy
from scipy.cluster.hierarchy import dendrogram, fcluster
import pandas
from .linkage import Linkage
from ._colormap import cmap_builder


class Corrplot(Linkage):
    """
    An implementation of correlation plotting tools (corrplot).
    the class requires `scipy <http://www.scipy.org/>`_.

    Here is a simple example with a correlation matrix as an input (stored in
    a pandas dataframe):

    .. plot::
        :width: 50%
        :include-source:

        import pandas
        import numpy
        letters = "ABCDEFGHIJKLM"[0:10]
        df = pandas.DataFrame(dict(( (k, numpy.random.random(10)+ord(k)-65) for k in letters)))

        import matplotlib.pyplot as plt
        plt.close('all')
        plt.style.use('ggplot')

        from pyensae.graph_helper import Corrplot
        c = Corrplot(df)
        c.plot()
        plt.show()

    This class requires module `colormap <https://pypi.python.org/pypi/colormap>`_.
    """

    def __init__(self, data, na=0):
        """
        Plots the content of square matrix that contains correlation values.

        :param data: input can be a dataframe (Pandas), or list of lists (python) or
            a numpy matrix. Note, however, that values must be between -1 and 1. If not,
            or if the matrix (or list of lists) is not squared, then correlation is
            computed. The data or computed correlation is stored in :attr:`df` attribute.
        :param na: replace NA values with this value (default 0)

        The :attr:`params` contains some tunable parameters for the colorbar in the
        :meth:`plot` method.

        ::

            # can be a list of lists, the correlation matrix is then a 2x2 matrix
            c = Corrplot([[1,1], [2,4], [3,3], [4,4]])

        """
        super(Corrplot, self).__init__()  # pylint: disable=R1725

        # we delay import in case this is not needed
        self.cmap_builder = cmap_builder

        self.df = pandas.DataFrame(data, copy=True)

        compute_correlation = False

        w, h = self.df.shape
        if self.df.max().max() > 1 or self.df.min().min() < -1:
            compute_correlation = True
        if w != h:
            compute_correlation = True
        if list(self.df.index) != list(self.df.columns):
            compute_correlation = True

        if compute_correlation:
            cor = self.df.corr()
            self.df = cor

        # replace NA with zero
        self.df.fillna(na, inplace=True)

        #: tunable parameters for the :meth:`plot` method.
        self.params = {
            'colorbar.N': 100,
            'colorbar.shrink': .8,
            'colorbar.orientation': 'vertical'}

    def _set_default_cmap(self):
        self.cm = self.cmap_builder('#AA0000', 'white', 'darkblue')

    def order(self, method='complete', metric='euclidean', inplace=False):
        """
        Rearranges the order of rows and columns after clustering.

        :param method: any scipy method (e.g., single, average, centroid,
            median, ward). See scipy.cluster.hierarchy.linkage
        :param metric: any scipy distance (euclidean, hamming, jaccard)
            See scipy.spatial.distance or scipy.cluster.hieararchy
        :param bool inplace: if set to True, the dataframe is replaced

        You probably do not need to use that method. Use :meth:`plot` and
        the two parameters order_metric and order_method instead.
        """
        if None is method or None is metric:
            return self.df
        Y = self.linkage(self.df, method=method, metric=metric)
        ind1 = fcluster(Y, 0.7 * max(Y[:, 2]), 'distance')
        Z = dendrogram(Y, no_plot=True)
        idx1 = Z['leaves']
        cor2 = self.df.iloc[idx1].T.iloc[idx1].T
        if inplace is True:
            self.df = cor2
        else:
            return cor2
        self.Y = Y
        self.Z = Z
        self.idx1 = idx1
        self.ind1 = ind1
        return cor2

    def plot(self, fig=None, grid=True,
             rotation=30, lower=None, upper=None,
             shrink=0.9, axisbg='white', colorbar=True, label_color='black',
             fontsize='small', edgecolor='black', method='ellipse',
             order_method='complete', order_metric='euclidean', cmap=None,
             ax=None, binarise_color=False, figsize=None):
        """
        Plots the correlation matrix from the content of :attr:`df`
        (dataframe).

        By default, the correlation is shown on the upper and lower triangle and is
        symmetric wrt to the diagonal. The symbols are ellipses. The symbols can
        be changed to e.g. rectangle. The symbols are shown on upper and lower sides but
        you could choose a symbol for the upper side and another for the lower side using
        the **lower** and **upper** parameters.

        :param fig: Create a new figure by default. If an instance of an existing
            figure is provided, the corrplot is overlayed on the figure provided.
            Can also be the number of the figure.
        :param grid: add grid (Defaults to grey color). You can set it to False or a color.
        :param rotation: rotate labels on y-axis
        :param lower: if set to a valid method, plots the data on the lower
            left triangle
        :param upper: if set to a valid method, plots the data on the upper
            left triangle
        :param float shrink: maximum space used (in percent) by a symbol.
            If negative values are provided, the absolute value is taken.
            If greater than 1, the symbols wiill overlap.
        :param axisbg: color of the background (defaults to white).
        :param colorbar: add the colorbar (defaults to True).
        :param str label_color: (defaults to black).
        :param fontsize: size of the fonts defaults to 'small'.
        :param method: shape to be used in 'ellipse', 'square', 'rectangle',
            'color', 'text', 'circle',  'number', 'pie'.

        :param order_method: see :meth:`order`.
        :param order_metric: see : meth:`order`.
        :param cmap: a valid cmap from matplotlib or colormap package (e.g.,
            'jet', or 'copper'). Default is red/white/blue colors.
        :param binarise_color: two colors only, negative, positive
        :param ax: a matplotlib axes.
        :param figsize: gives that parameter to the new created figure
        :return: ax (matplotlib axes)

        The colorbar can be tuned with the parameters stored in :attr:`params`.
        Here is an example. See notebook for other examples:

        ::

            c = corrplot.Corrplot(dataframe)
            c.plot(cmap=('Orange', 'white', 'green'))
            c.plot(method='circle')
            c.plot(colorbar=False, shrink=.8, upper='circle'  )
        """
        import matplotlib.pyplot as plt  # pylint: disable=C0415

        # default
        if cmap is not None:
            try:
                if isinstance(cmap, str):
                    self.cm = self.cmap_builder(cmap)
                else:
                    self.cm = self.cmap_builder(*cmap)
            except Exception:
                self._set_default_cmap()
        else:
            self._set_default_cmap()

        self.shrink = abs(shrink)
        self.fontsize = fontsize
        self.edgecolor = edgecolor

        df = self.order(method=order_method, metric=order_metric)

        # figure can be a number or an instance; otherwise creates it
        params = dict(facecolor=axisbg)
        if isinstance(fig, int):
            params["num"] = fig.number
        elif fig is not None:
            params["num"] = fig.number
        else:
            params["num"] = None
        if figsize is not None:
            params["figsize"] = figsize
        fig = plt.figure(**params)

        # do we have an axes to plot the data in ?
        if ax is None:
            ax = plt.subplot(1, 1, 1, aspect='equal', facecolor=axisbg)
        else:
            # if so, clear the axes. Colorbar cannot be removed easily.
            plt.sca(ax)
            ax.clear()

        # subplot resets the bg color, let us set it again
        fig.set_facecolor(axisbg)

        width, height = df.shape
        labels = (df.columns)

        if upper is None and lower is None:
            mode = 'method'
        elif upper and lower:
            mode = 'both'
        elif lower is not None:
            mode = 'lower'
        elif upper is not None:
            mode = 'upper'

        self.binarise_color = binarise_color
        if mode == 'upper':
            self._add_patches(df, upper, 'upper', ax, diagonal=True)
        elif mode == 'lower':
            self._add_patches(df, lower, 'lower', ax, diagonal=True)
        elif mode == 'method':
            self._add_patches(df, method, 'both', ax, diagonal=True)
        elif mode == 'both':
            self._add_patches(df, upper, 'upper', ax, diagonal=False)
            self._add_patches(df, lower, 'lower', ax, diagonal=False)

        # shift the limits to englobe the patches correctly
        ax.set_xlim(-0.5, width - .5)
        ax.set_ylim(-0.5, height - .5)

        # set xticks/xlabels on top
        ax.xaxis.tick_top()
        xtickslocs = numpy.arange(len(labels))
        ax.set_xticks(xtickslocs)
        ax.set_xticklabels(labels, rotation=rotation, color=label_color,
                           fontsize=fontsize, ha='left')

        ax.invert_yaxis()
        ytickslocs = numpy.arange(len(labels))
        ax.set_yticks(ytickslocs)
        ax.set_yticklabels(labels, fontsize=fontsize, color=label_color)
        plt.tight_layout()

        if grid is not False:
            if grid is True:
                grid = 'grey'
            for i in range(0, width):
                ratio1 = float(i) / width
                ratio2 = float(i + 2) / width
                # set axis off
                # 2 - set xlabels along the diagonal
                # set colorbar either on left or bottom
                if mode == 'lower':
                    ax.axvline(i + .5, ymin=1 - ratio1, ymax=0., color=grid)
                    ax.axhline(i + .5, xmin=0, xmax=ratio2, color=grid)
                if mode == 'upper':
                    ax.axvline(i + .5, ymin=1 - ratio2, ymax=1, color=grid)
                    ax.axhline(i + .5, xmin=ratio1, xmax=1, color=grid)
                if mode in ['method', 'both']:
                    ax.axvline(i + .5, color=grid)
                    ax.axhline(i + .5, color=grid)

            # can probably be simplified
            if mode == 'lower':
                ax.axvline(-.5, ymin=0, ymax=1, color='grey')
                ax.axvline(width - .5, ymin=0, ymax=1. /
                           width, color='grey', lw=2)
                ax.axhline(width - .5, xmin=0, xmax=1, color='grey', lw=2)
                ax.axhline(-.5, xmin=0, xmax=1. / width, color='grey', lw=2)
                ax.xticks([])
                for i in range(0, width):
                    ax.text(i, i - .6, labels[i], fontsize=fontsize,
                            color=label_color,
                            rotation=rotation, verticalalignment='bottom')
                    ax.text(-.6, i, labels[i], fontsize=fontsize,
                            color=label_color,
                            rotation=0, horizontalalignment='right')
                ax.set_axis_off()
            # can probably be simplified
            elif mode == 'upper':
                ax.axvline(width - .5, ymin=0, ymax=1, color='grey', lw=2)
                ax.axvline(-.5, ymin=1 - 1. / width,
                           ymax=1, color='grey', lw=2)
                ax.axhline(-.5, xmin=0, xmax=1, color='grey', lw=2)
                ax.axhline(width - .5, xmin=1 - 1. / width,
                           xmax=1, color='grey', lw=2)
                ax.yticks([])
                for i in range(0, width):
                    ax.text(-.6 + i, i, labels[i], fontsize=fontsize,
                            color=label_color, horizontalalignment='right',
                            rotation=0)
                    ax.text(i, -.5, labels[i], fontsize=fontsize,
                            color=label_color, rotation=rotation, verticalalignment='bottom')
                ax.set_axis_off()

        # set all ticks length to zero
        ax = plt.gca()
        ax.tick_params(axis='both', which='both', length=0)

        if colorbar:
            N = self.params['colorbar.N'] + 1
            if N < 2:
                raise RuntimeError("No colorbar to draw.")
            cb = plt.gcf().colorbar(
                self.collection, orientation=self.params['colorbar.orientation'],
                shrink=self.params['colorbar.shrink'],
                boundaries=numpy.linspace(0, 1, N),
                ticks=[0, .25, 0.5, 0.75, 1])
            cb.ax.set_yticklabels([-1, -.5, 0, .5, 1])
            # make sure it goes from -1 to 1 even though actual values may not
            # reach that range
            # cb.set_clim(0, 1)
            # not working in matplotlib 3.3.0

        return ax

    def _add_patches(self, df, method, fill, ax, diagonal=True):

        from matplotlib.patches import Ellipse, Circle, Rectangle, Wedge
        from matplotlib.collections import PatchCollection

        width, height = df.shape

        patches = []
        colors = []
        for x in range(width):
            for y in range(height):
                if fill == 'lower' and x > y:
                    continue
                if fill == 'upper' and x < y:
                    continue
                if diagonal is False and x == y:
                    continue
                datum = (df.iloc[x, y] + 1.) / 2.
                d = df.iloc[x, y]
                d_abs = numpy.abs(d)
                #c = self.pvalues[x, y]
                rotate = -45 if d > 0 else +45
                #cmap = self.poscm if d >= 0 else self.negcm
                if method in ['ellipse', 'square', 'rectangle', 'color']:
                    if method == 'ellipse':
                        func = Ellipse
                        patch = func((x, y), width=1 * self.shrink,
                                     height=(self.shrink - d_abs * self.shrink), angle=rotate)
                    else:
                        func = Rectangle
                        w = h = d_abs * self.shrink
                        offset = (1 - w) / 2.
                        if method == 'color':
                            w = 1
                            h = 1
                            offset = 0
                        patch = func((x + offset - .5, y + offset - .5), width=w,
                                     height=h, angle=0)
                    if self.edgecolor:
                        patch.set_edgecolor(self.edgecolor)
                    # patch.set_facecolor(cmap(d_abs))
                    colors.append(datum)
                    if d_abs > 0.05:
                        patch.set_linestyle('dotted')
                    # ax.add_artist(patch)
                    patches.append(patch)
                elif method == 'circle':
                    patch = Circle((x, y), radius=d_abs * self.shrink / 2.)
                    if self.edgecolor:
                        patch.set_edgecolor(self.edgecolor)
                    # patch.set_facecolor(cmap(d_abs))
                    colors.append(datum)
                    if d_abs > 0.05:
                        patch.set_linestyle('dotted')
                    # ax.add_artist(patch)
                    patches.append(patch)
                elif method in ['number', 'text']:
                    if d < 0:
                        edgecolor = self.cm(-1.0)
                    elif d >= 0:
                        edgecolor = self.cm(1.0)
                    d_str = "{:.2f}".format(d).replace(
                        "0.", ".").replace(".00", "")
                    ax.text(x, y, d_str, color=edgecolor,
                            fontsize=self.fontsize, horizontalalignment='center',
                            weight='bold', alpha=max(0.5, d_abs),
                            withdash=False)
                elif method == 'pie':
                    S = 360 * d_abs
                    patch = [
                        Wedge((x, y), 1 * self.shrink / 2., -90, S - 90),
                        Wedge((x, y), 1 * self.shrink / 2., S - 90, 360 - 90),
                    ]
                    # patch[0].set_facecolor(cmap(d_abs))
                    # patch[1].set_facecolor('white')
                    colors.append(datum)
                    colors.append(0.5)
                    if self.edgecolor:
                        patch[0].set_edgecolor(self.edgecolor)
                        patch[1].set_edgecolor(self.edgecolor)

                    # ax.add_artist(patch[0])
                    # ax.add_artist(patch[1])
                    patches.append(patch[0])
                    patches.append(patch[1])
                else:
                    raise ValueError(
                        'Method for the symbols is not known. Use e.g, square, circle')

        if self.binarise_color:
            colors = [1 if color > 0.5 else -1 for color in colors]

        if len(patches):
            col1 = PatchCollection(
                patches, array=numpy.array(colors), cmap=self.cm)
            ax.add_collection(col1)

            self.collection = col1
