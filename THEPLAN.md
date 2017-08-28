
## Context:

* We have two blocks of time: 9:30-10:30 and 11-12:30
* We are first, so no one has battle-tested their Python installations
* There are ~55 attendees - for the tutorial part, I think that means we aim to
  split into 10 groups of 5 with a few expert floaters (Tollerud, Vanderplas,
  Leistedt, Huppenkothen, Barbary)

## Generating the groups:

* We form groups by asking questions of increasing difficulty until there are
  ~10 people with hands up
* For example, "Keep your hand raised if you agree with the following
  statements":
    * I've used Python
    * I've used Python in my research
    * I've used Numpy
    * I'm very comfortable with Numpy
    * I've used scikit-learn
    * I'm very comfortable with scikit-learn
* We end when ~10 people are left standing, and we each of those people a number
* We then count out everyone else to randomize the room a bit
* Each group will do a supervised problem, and an unsupervised problem.

## Data:

### Note: these are real-world data!

* The projects we're giving you are close to real projects, so they could turn
  into real projects to work on during the week! Talk to us if interested.

#### SDSS (BOSS) spectra:

* 100,000 BOSS spectra from 100 plates (including sky fibers, etc.) and their
  inverse-variance arrays. All are on the same wavelength grid.
* Catalog info from the spectroscopic pipeline for all targets (from
  `specObj-dr14.fits`)
* Photometric info from the photometric pipeline for all targets (from the
  `photoPosPlate-*.fits` files)

*Projects:*

* (*supervised*) Predict colors from spectrum
* (*unsupervised*) PCA the spectra themselves

#### Gaia TGAS astrometry + 2MASS and WISE photometry:

* ~2 million sources in the Gaia TGAS catalog (sky positions, proper motions,
  parallax) along with position-matched photometry from 2MASS and WISE (from the
  Gaia archive)
* Classification problem: RG / MS
* Regression problem: predict W1, W2 given TGAS + 2MASS

## Group stage

* Divide in to 10 groups 0-9
* Odd groups = SDSS, Even groups = Gaia
* floor(Group number / 2)
  * 0 : k-means (unsupervised clustering)
  * 1 : kernel SVM (supervised classification)
  * 2 : logistic regression (supervised regression)
  * 3 : t-SNE (unsupervised dim. red.)
  * 4 : GMM (if SDSS, on first <10 PCA components) (unsupervised density est.)
* Within each group, each person will help with everything, but each person is
  the "lead" on a specific role (that they self-organize to assign):
    * *Data munger*: Turn data into matrix `X` and vector `y` for supervised,
      matrix `X` only for unsupervised. After pre-processing, generate separate
      Train and Test data for supervised.
    * *Preprocessor*: Data quality cuts (e.g., on parallax quality).
      Normalization? (e.g., normalize spectra for SDSS? Throw away sky fibers?)
      Shift spectra to rest-frame or work in a bin in catalog parameters?
      Restrict to a single class (e.g., just take stars?) Cut a small region
      around, e.g., 5000 Angstroms rest frame.
    * *Visualizer*: (1) take pre-processed data, show that the data look ok to
      feed into a ML method (not too much crap), (2) plot confusion matrix, ROC
      curves, cross-validation score. Demonstrate that the machine learning
      method did *something* sensible.
    * *Methodizer*: Be ready to take the rectangular data (`X`, maybe `X`, `y`),
      train a scikit-learn model, experiment with any hyper-parameters.
    * *Presenter*: Summarize what your group did, show plots.

## Proposed plan:

* **9:30-10:30:**
    * Basic intro to terminology, general problems (*~15-20 mins* of talking)
        * Supervised vs. Unsupervised - then classification, regression,
          clustering, dimensionality reduction, density estimation
        * Cross-validation
        * Resources to learn more (books? online courses? e.g., Andrew Ng)
    * As an example of supervised, explain k-nearest neighbors and implement
      together (will have most code ready in a notebook) (*~10-15 minutes*)
    * As an example of unsupervised, explain PCA and implement together (will
      have most code ready in a notebook) (*~10-15 minutes*)
    * Demo how easy it is to do the above to with scikit-learn - all methods
      have the same API, very easy to extend
        * Re-do PCA together using scikit-learn
* **10:30-11:00**:
    * Coffee break and helping people with installation issues.
* **11:00-12:00**:
    * Group working
* **12:00-12:30**::
    * Present results
    * 3 minutes per group

## Breakout: the woes of machine learning

Jake VDP + APW?
