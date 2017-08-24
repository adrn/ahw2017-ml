
## Context:

* We have two blocks of time: 9:30-10:30 and 11-12:30
* We are first, so no one has battle-tested their Python installations
* There are ~55 attendees - for the tutorial part, I think that means we aim to
  split into 10 groups of 5 with a few expert floaters (Tollerud, Vanderplas,
  Leistedt, Huppenkothen, Barbary)

## Groups:

* We form groups by asking questions of increasing difficulty until there are
  ~10 people with hands up
* For example, "Keep your hand raise if you agree with the following statements":
    * I've used Python
    * I've used Python in my research
    * I've used Numpy
    * I'm very comfortable with Numpy
    * I've used scikit-learn
    * I'm very comfortable with scikit-learn
* We end when ~10 people are left standing, and we each of those people a number
* We then count out everyone else to randomize the room a bit
* Within each group, each person will help with everything, but each person is
  the "lead" on a specific role (that they self-organize to assign):
    * *Data munger*: Turn data into matrix X and vector y for supervised, matrix
      X for unsupervised. Generate separate Train and Test data for supervised.
    * *Model trainer*: Take data, train a scikit-learn model for their assigned
      method, experiment with any hyper-parameters
    * (**supervised**) *Cross-validator*: Improve the accuracy of the model by
      setting hyper-parameters using cross-validation.
    * (**unsupervised**) TODO: what is the analog to cross-validator for
      unsupervised?
    * *Visualizer*: Make plots to visualize the results (TODO: give specific
      plot suggestions)
    * *Presenter*: Summarize what your group did, show plots

## Data:

#### SDSS (BOSS) spectra:

* 100,000 BOSS spectra from 100 plates (including sky fibers, etc.)
* Catalog info from the spectroscopic pipeline for all targets (from
  `specObj-dr14.fits`)
* Photometric info from the photometric pipeline for all targets (from the
  `photoPosPlate-*.fits` files)

*Projects:*

* TODO

#### Gaia TGAS astrometry + 2MASS and WISE photometry:

* ~2 million sources in the Gaia TGAS catalog (sky positions, proper motions,
  parallax) along with position-matched photometry from 2MASS and WISE (from the
  Gaia archive)

*Projects:*

* TODO

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
