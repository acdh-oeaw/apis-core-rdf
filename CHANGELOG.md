# Changelog

## [0.16.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.15.2...v0.16.0) (2024-03-27)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** drop RootObject.deprecated_name

### Features

* **apis_entities:** surround navigation elements with block ([6b2fb49](https://github.com/acdh-oeaw/apis-core-rdf/commit/6b2fb494131d1333f5ac04bf9ddef826aac7bdf8))
* **apis_relations:** add and use PropertySubjObjFilter ([246b7f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/246b7f3fa0f530c605f892bd6866719b4a9e427a))
* **generic:** add ContentTypeInstanceSerializer ([3307074](https://github.com/acdh-oeaw/apis-core-rdf/commit/33070747df9aad9bb51424ec433a9f389aeeee9a))
* **generic:** implement custom schema generator ([09a1d6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/09a1d6d932028781a57b866397f0d94e6be5cd15))
* **generic:** introduce GenericFilterBackend and use it ([dac1f6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/dac1f6dc970d634e2f456ccbf46e4395949a9188))
* **generic:** ship a JSON based and a newline based list widget ([8704d21](https://github.com/acdh-oeaw/apis-core-rdf/commit/8704d2154a936b18f4db7d0b68452ca74295fb88)), closes [#733](https://github.com/acdh-oeaw/apis-core-rdf/issues/733)


### Bug Fixes

* **apis_metainfo:** drop RootObject.deprecated_name ([5fc11d7](https://github.com/acdh-oeaw/apis-core-rdf/commit/5fc11d7750171ead51c9242cd0480f27b039d72b))
* **apis_relations:** reuse GenericTable.Meta.sequence for tables ([b15e587](https://github.com/acdh-oeaw/apis-core-rdf/commit/b15e5875ae78e4dda28413856a67929a96a08bd3)), closes [#716](https://github.com/acdh-oeaw/apis-core-rdf/issues/716)
* **generic:** fix typo in Import View ([b28de6e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b28de6e430b874f96abdfa2b84b6551537a15b58))
* **generic:** use fallback if ModelViewSet attributes don't exist ([11e097d](https://github.com/acdh-oeaw/apis-core-rdf/commit/11e097d64b949f8171f44d1f26238c2ba6aeaad0))

## [0.15.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.15.1...v0.15.2) (2024-03-19)


### Bug Fixes

* **apis_entities:** don't duplicate equal values when mergin charfield ([67f2aa5](https://github.com/acdh-oeaw/apis-core-rdf/commit/67f2aa5d5f6836bd5aa27fb0cace2f7784ea91a0))
* **apis_metainfo:** use ContentType instead of custom caching ([58e6c25](https://github.com/acdh-oeaw/apis-core-rdf/commit/58e6c25a134ae3ef760d0e724c721d0ecb975cd3))
* **core:** drop webpage remains from template ([6b3573e](https://github.com/acdh-oeaw/apis-core-rdf/commit/6b3573e4dff37a15dac33c54f9a9d3d3bd45e127)), closes [#410](https://github.com/acdh-oeaw/apis-core-rdf/issues/410)
* **core:** remove hardcoded imprint pointing to 404 ([e8441d9](https://github.com/acdh-oeaw/apis-core-rdf/commit/e8441d965ecb87f6f9925889c1f4b88d3d8e5e1c)), closes [#415](https://github.com/acdh-oeaw/apis-core-rdf/issues/415)
* **generic:** typo in `module_paths` argument ([3f3b71e](https://github.com/acdh-oeaw/apis-core-rdf/commit/3f3b71e125eafa47193f4285ea241830b80dfd63))
* **generic:** use `import_string` instead of custom method ([591b1ca](https://github.com/acdh-oeaw/apis-core-rdf/commit/591b1ca9ccb1bd1cd0288fe48de2cdbc75599b89)), closes [#697](https://github.com/acdh-oeaw/apis-core-rdf/issues/697)

## [0.15.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.15.0...v0.15.1) (2024-03-11)


### Bug Fixes

* **utils:** make rdfimport parent model check more loose ([84b97d3](https://github.com/acdh-oeaw/apis-core-rdf/commit/84b97d341757365deb4abf2cff846306d9a5249f))

## [0.15.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.14.2...v0.15.0) (2024-03-07)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** The renaming of RootObject's "name" field to "deprecated_name" affects all inheriting model classes as well as class Property. You will need to create new fields in your model classes to replace it/to preserve its contents before it gets dropped.
* **core:** projects using the `confirm_delete.html` template will have to change that. There is a replacement in `generic/generic_confirm_delete.html`.
* **apis_metainfo,apis_entities:** drop __str___ overrides

### Features

* **apis_entities:** implement default abstract entity classes ([b1ebd0a](https://github.com/acdh-oeaw/apis-core-rdf/commit/b1ebd0a7b4c5c388c65aa36704521f646c8aed64)), closes [#403](https://github.com/acdh-oeaw/apis-core-rdf/issues/403)
* **apis_relations:** add obj and subj class filter to triple filters ([4b890c4](https://github.com/acdh-oeaw/apis-core-rdf/commit/4b890c47ad97ec0579db3892d2d7d562cf5a7d2a)), closes [#668](https://github.com/acdh-oeaw/apis-core-rdf/issues/668)
* **generic:** allow to override serializer based on renderer ([676251d](https://github.com/acdh-oeaw/apis-core-rdf/commit/676251de08c58266dabdc37038a43e2deab7114d))


### Bug Fixes

* **apis_entities:** move duplicate button after other action buttons ([1683968](https://github.com/acdh-oeaw/apis-core-rdf/commit/1683968b1a994c155a5f4e36ec96cf2ee517d1c2)), closes [#694](https://github.com/acdh-oeaw/apis-core-rdf/issues/694)
* **apis_entities:** use `modelname` instead of `verbose_name` ([ef10a69](https://github.com/acdh-oeaw/apis-core-rdf/commit/ef10a69ba8e66d86f42128789b7facdc9e39df73))
* **apis_entities:** use modelname instead of verbose_name in javascript ([6fee852](https://github.com/acdh-oeaw/apis-core-rdf/commit/6fee852c3ee1084b7d4ad345efaf2a6464f16370))
* **generic:** pass existing queryset to custom queryset ([12d4ed8](https://github.com/acdh-oeaw/apis-core-rdf/commit/12d4ed8c22eeb584df122d1c37cde7e1ee780d6a))


### Code Refactoring

* **apis_metainfo,apis_entities:** drop __str___ overrides ([c9fbcc8](https://github.com/acdh-oeaw/apis-core-rdf/commit/c9fbcc8f43320dbe1a0b188b14a0a8939fadbe81))
* **apis_metainfo:** rename RootObject.name to deprecated_name ([fcd4854](https://github.com/acdh-oeaw/apis-core-rdf/commit/fcd485453e88f5247f56c0f92f78ab3772852ece)), closes [#299](https://github.com/acdh-oeaw/apis-core-rdf/issues/299)
* **core:** drop unused template ([391f2de](https://github.com/acdh-oeaw/apis-core-rdf/commit/391f2dea9d0452e40efcc1f312497941c1ce99ff)), closes [#518](https://github.com/acdh-oeaw/apis-core-rdf/issues/518)

## [0.14.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.14.1...v0.14.2) (2024-02-29)


### Bug Fixes

* **apis_metainfo:** let Collection inherit from GenericModel ([0e32a80](https://github.com/acdh-oeaw/apis-core-rdf/commit/0e32a804c322b4b6448342d9f0f04b2cca0e04a5))

## [0.14.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.14.0...v0.14.1) (2024-02-29)


### Bug Fixes

* **generic,core:** move htmx setup from generic template to base.html ([bc4ba98](https://github.com/acdh-oeaw/apis-core-rdf/commit/bc4ba98033db560a02bff058938bdafebc8ecfb9))
* **generic:** use serializer_factory even with custom serializers ([247200e](https://github.com/acdh-oeaw/apis-core-rdf/commit/247200ebc075e557e450a92447ceb54ffa0fb72b))

## [0.14.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.13.1...v0.14.0) (2024-02-27)


### ⚠ BREAKING CHANGES

* **generic:** projects will have to inherit from `GenericModel` from now on, if they want their models to be accessible via the generic views. Models inheriting from APIS models automatically inherit from `GenericModel`.

### Features

* **generic:** use lru cache for smaller methods ([7e56e48](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e56e480a141e81c5920df022e3d66e0c5c193ff))
* **utils:** provide some abstract base classes for autocomplete ([b3d2cbe](https://github.com/acdh-oeaw/apis-core-rdf/commit/b3d2cbecb34eb2e680139e9b57e502dbb561d558)), closes [#653](https://github.com/acdh-oeaw/apis-core-rdf/issues/653)


### Bug Fixes

* **apis_entities:** make import form deal with html data ([e7882e2](https://github.com/acdh-oeaw/apis-core-rdf/commit/e7882e253d950416d46f27af6c7b994e2362b838))
* **apis_entities:** remove buggy jQuery code ([f4fd17e](https://github.com/acdh-oeaw/apis-core-rdf/commit/f4fd17e21897eecc2f8801ffefef0267c0fe0fa6)), closes [#529](https://github.com/acdh-oeaw/apis-core-rdf/issues/529)
* **apis_relations:** remove choice limit in Property ([babfe4e](https://github.com/acdh-oeaw/apis-core-rdf/commit/babfe4ecabb3567b00e2970048e3ea653f20c0c4)), closes [#412](https://github.com/acdh-oeaw/apis-core-rdf/issues/412)
* **generic:** add `__init__.py` to generic module ([a74d445](https://github.com/acdh-oeaw/apis-core-rdf/commit/a74d4457de1567c1c0e911624ea508f195da95cb))
* **utils:** make rdf parser more robust ([d3ba5e3](https://github.com/acdh-oeaw/apis-core-rdf/commit/d3ba5e369b9eb2a88eb101b2adefadc7402ce85f)), closes [#666](https://github.com/acdh-oeaw/apis-core-rdf/issues/666)
* **utils:** refactor `access_for_all` ([b021696](https://github.com/acdh-oeaw/apis-core-rdf/commit/b0216968d67b21e1374968156e898a92e0cd831d)), closes [#582](https://github.com/acdh-oeaw/apis-core-rdf/issues/582)


### Documentation

* cleanup configuration section and rename it to `settings` ([d2c141c](https://github.com/acdh-oeaw/apis-core-rdf/commit/d2c141cb835df8cbdc1691e533b9a2ab61e30808))
* **generic:** add documentation about `GenericModel` ([54fbb09](https://github.com/acdh-oeaw/apis-core-rdf/commit/54fbb09e89d04b15b8eb38ec5af85263f7e4eb5b))


### Code Refactoring

* **generic:** introduce `generic.abc.GenericModel` ([8a58abc](https://github.com/acdh-oeaw/apis-core-rdf/commit/8a58abcc817267808c55a2d187d3dfe230599de8)), closes [#657](https://github.com/acdh-oeaw/apis-core-rdf/issues/657)

## [0.13.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.13.0...v0.13.1) (2024-02-15)


### Bug Fixes

* **apis_entities:** hide duplicate button on missing permission ([096181f](https://github.com/acdh-oeaw/apis-core-rdf/commit/096181fdaaca4fbb3caa4d06260e19abb2290acb))
* **apis_relations:** linkify subject and object columns ([bd1ed3d](https://github.com/acdh-oeaw/apis-core-rdf/commit/bd1ed3d45bdbcbba9979cbb586de0bdbb5dc8937)), closes [#1](https://github.com/acdh-oeaw/apis-core-rdf/issues/1)
* **generic:** check for permissions in actions nav ([0ec25df](https://github.com/acdh-oeaw/apis-core-rdf/commit/0ec25dfae9d7b7802521a1916a13e40506036fdd))
* **generic:** hide create button if permission does not exist ([154d2dd](https://github.com/acdh-oeaw/apis-core-rdf/commit/154d2dd3928f801fbb3a93671baf42118d31d3de))
* **generic:** the relevant permission name is `change` not `edit` ([fcdb491](https://github.com/acdh-oeaw/apis-core-rdf/commit/fcdb491b17814733a50f9b77d833ea59bb1891c9))
* **generic:** use custom permission solution in views ([edb783e](https://github.com/acdh-oeaw/apis-core-rdf/commit/edb783ec69eb790a936c2cdf4dd4b65c09ca8f89))

## [0.13.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.6...v0.13.0) (2024-02-14)


### ⚠ BREAKING CHANGES

* **apis_entities:** with the removal of `filters.py` and `tables.py` your configuration in `APIS_ENTITIES` won't have any effect anymore. Please replace them with custom tables and custom filtersets. Also the the locations and names and structure of the templates changed, so you will have to update those.

### Features

* add collection name as css class to collection templates ([44e1cf1](https://github.com/acdh-oeaw/apis-core-rdf/commit/44e1cf128aab9b214f245da7019e74a4f7ec2490)), closes [#604](https://github.com/acdh-oeaw/apis-core-rdf/issues/604)
* **generic:** add debug log message to first_match_via_mro ([458ffd2](https://github.com/acdh-oeaw/apis-core-rdf/commit/458ffd2178532f6eac11c443374515be26e74c56))
* **generic:** display foreign key fields as value instead of id ([7936d8a](https://github.com/acdh-oeaw/apis-core-rdf/commit/7936d8aaaacb66dfee6a2a7f4534bdd525196cb3))
* **generic:** fix and enhance the generate_search_filter helper ([03eb3fe](https://github.com/acdh-oeaw/apis-core-rdf/commit/03eb3fe9c08f04ba676ff06de35aed496e12cf2a))
* **generic:** make GenericImporter more verbose ([63aa960](https://github.com/acdh-oeaw/apis-core-rdf/commit/63aa9600e8a42486d4a3fc41420ef6524f8d9261))
* **generic:** use `data-html` in autocomplete widgets ([c6d326f](https://github.com/acdh-oeaw/apis-core-rdf/commit/c6d326f676e039550abb8f4fda420cb9843c5aeb))
* **generic:** use template attribute of autocomplete view ([a9f0d38](https://github.com/acdh-oeaw/apis-core-rdf/commit/a9f0d38dc5a9850421ddfee60a335a8100aa84d3))
* **utils:** use dict_from_toml_directory for cleaning uris ([a703f51](https://github.com/acdh-oeaw/apis-core-rdf/commit/a703f513931e5cf957c8499f1ba1dfa05d79f728))


### Bug Fixes

* **apis_entities:** f string in merge_textfield missing f ([2b7bdb9](https://github.com/acdh-oeaw/apis-core-rdf/commit/2b7bdb951410deae0dee4443d77cdacf06d5be65))
* **apis_entities:** fix wikidata uri mapping ([7372ff1](https://github.com/acdh-oeaw/apis-core-rdf/commit/7372ff16f7e7688561ca81aaef4ba68d0cf613e5))
* **apis_metainfo:** set the `alters_data` attribute of duplicate ([d5cfdb5](https://github.com/acdh-oeaw/apis-core-rdf/commit/d5cfdb55cb005d3967bfd04aad7130526225d93b))
* **apis_relations:** don't rely on APIS_BASE_URI for editing relations ([39f2cf1](https://github.com/acdh-oeaw/apis-core-rdf/commit/39f2cf189cb0705bc03efd40664db8da7754ec8b))
* **apis_relations:** use generic autocomplete in GenericTripleForm ([0b23cc7](https://github.com/acdh-oeaw/apis-core-rdf/commit/0b23cc7c7535e945ee36b2213aa5350f495476d6))
* **generic:** don't set template_name_suffix, only use it if its set ([71aef12](https://github.com/acdh-oeaw/apis-core-rdf/commit/71aef12645aa8b4a5b655a1e0cac40e54255ba54))
* **generic:** redirect to update view after create or update ([1faf5c4](https://github.com/acdh-oeaw/apis-core-rdf/commit/1faf5c472cd5f65e648bef99c89a3964d10b452d))


### Documentation

* **generic:** add documentation about generic app customization ([6de3708](https://github.com/acdh-oeaw/apis-core-rdf/commit/6de370891d0b450afc44eefd1062a899dcfcdfec))


### Code Refactoring

* **apis_entities:** use new generic app ([45de48b](https://github.com/acdh-oeaw/apis-core-rdf/commit/45de48bea2b81823873066820a079635b8d7a04a))

## [0.12.6](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.5...v0.12.6) (2024-01-31)


### Bug Fixes

* let the autocomplete form create objects ([a07f23b](https://github.com/acdh-oeaw/apis-core-rdf/commit/a07f23beed83614832c085b6de0f9a46008eb34f))

## [0.12.5](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.4...v0.12.5) (2024-01-31)


### Bug Fixes

* exclude `metadata` field from legacy api viewset stuff ([dd2fb57](https://github.com/acdh-oeaw/apis-core-rdf/commit/dd2fb578b99e7a8cebd388576c6ad10971a889be))

## [0.12.4](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.3...v0.12.4) (2024-01-31)


### Bug Fixes

* **generic:** don't allow access to `admin`, `auth` and `sessions` ([ff43fc8](https://github.com/acdh-oeaw/apis-core-rdf/commit/ff43fc846ca94718b1d23533a1d836e92c8c0ef5))

## [0.12.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.2...v0.12.3) (2024-01-31)


### Bug Fixes

* **apis_entities:** add more information to autocomplete results ([db1c0c7](https://github.com/acdh-oeaw/apis-core-rdf/commit/db1c0c73b038e93e75feb0a71e691f1bb2c0ea13))
* **generic:** only show table actions if user has required permissions ([79d74a3](https://github.com/acdh-oeaw/apis-core-rdf/commit/79d74a317aa3e2b8a50595b81456f72f21a4ae5e)), closes [#584](https://github.com/acdh-oeaw/apis-core-rdf/issues/584)

## [0.12.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.1...v0.12.2) (2024-01-30)


### Bug Fixes

* use the ListViewObjectFilterMixin in the generic.views.List view ([94734dc](https://github.com/acdh-oeaw/apis-core-rdf/commit/94734dc425333edf04b1f0f9268dcf9941ce79f1))

## [0.12.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.12.0...v0.12.1) (2024-01-30)


### Bug Fixes

* **api_routers:** fix generic_serializer_creation_factory ([eeb7430](https://github.com/acdh-oeaw/apis-core-rdf/commit/eeb743086cb9cca725e7f9401d2e028302db467b)), closes [#577](https://github.com/acdh-oeaw/apis-core-rdf/issues/577)
* drop TextSerializer and use GenericHyperlinkedModelSerializer ([5c0091b](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c0091baee43515ca9bc2fff5e18f52f789e2c97))

## [0.12.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.3...v0.12.0) (2024-01-30)


### Features

* **generic:** allow to extend autocomplete results with custom results ([cbad572](https://github.com/acdh-oeaw/apis-core-rdf/commit/cbad572207d419e5a8ed5be1d8bb8315054cd407))
* **generic:** implement extendable importer ([06ad57b](https://github.com/acdh-oeaw/apis-core-rdf/commit/06ad57b629c912f9419024e77bc4aff299a518fe)), closes [#541](https://github.com/acdh-oeaw/apis-core-rdf/issues/541)


### Documentation

* document extending the autocomplete endpoint ([8f1613b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8f1613b7b52cede4d58962e4b6fbf2c434f4be16))
* document importing data from external resources ([280413e](https://github.com/acdh-oeaw/apis-core-rdf/commit/280413e4fe607d6a5500484a527840c0bf736058))
* update readme ([bba2c8c](https://github.com/acdh-oeaw/apis-core-rdf/commit/bba2c8c0b8acbe16f45f8414d5970de4cc6c3bee))

## [0.11.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.2...v0.11.3) (2024-01-26)


### Bug Fixes

* **apis_entities:** fix accidently removed form save ([33792cc](https://github.com/acdh-oeaw/apis-core-rdf/commit/33792cc277360d73abc4b88cd2be6a9addc8ca7e))

## [0.11.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.1...v0.11.2) (2024-01-26)


### Bug Fixes

* add missing skoscollection migration ([7c8d861](https://github.com/acdh-oeaw/apis-core-rdf/commit/7c8d861341747efa49cb795f03b75cf181ea1d22))
* **generic:** the permission string must also contain the app_label ([8140a3d](https://github.com/acdh-oeaw/apis-core-rdf/commit/8140a3db3e6b95550947a1254cde2ad1ec9d2fc8))

## [0.11.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.11.0...v0.11.1) (2024-01-25)


### Bug Fixes

* **collections:** add collection_content_objects templatetag ([865754a](https://github.com/acdh-oeaw/apis-core-rdf/commit/865754abe1926d7fde4e6db6edb4fb24790d8c52))
* **collections:** set default order of SkosCollection ([88543d2](https://github.com/acdh-oeaw/apis-core-rdf/commit/88543d2db2b15ea4fc4095402b4cd9f956fd5110))
* let users override generic views ([7b30880](https://github.com/acdh-oeaw/apis-core-rdf/commit/7b308808969503a5ea97b304e8f310247e9c45d3))

## [0.11.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.10.1...v0.11.0) (2024-01-24)


### Features

* add collections app ([6e6753e](https://github.com/acdh-oeaw/apis-core-rdf/commit/6e6753e15a4aa905634805e40d58f97191c60f92))
* allow to exclude fields from table columns ([92cba82](https://github.com/acdh-oeaw/apis-core-rdf/commit/92cba8214e02e4b0cfc081016821e234f389a5da))


### Documentation

* add documentation for new collections app ([e5020be](https://github.com/acdh-oeaw/apis-core-rdf/commit/e5020be1eab755b99b80285b9885ae5b155f817f))

## [0.10.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.10.0...v0.10.1) (2024-01-19)


### Bug Fixes

* **generic:** backport `filterset_factory` from django-filters ([c235107](https://github.com/acdh-oeaw/apis-core-rdf/commit/c235107154ab50a1e90b9a5f1aba8d324fdc0df9))
* **generic:** filter the iterator before returning the first element ([a6fba0f](https://github.com/acdh-oeaw/apis-core-rdf/commit/a6fba0f0d362158d768926196733567d392f983c))

## [0.10.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.9.1...v0.10.0) (2024-01-18)


### ⚠ BREAKING CHANGES

* **apis_entities:** drop TempEntityClass
* **apis_vocabularies:** remove apis_vocabularies app

### Features

* add htmx to base template ([f33b707](https://github.com/acdh-oeaw/apis-core-rdf/commit/f33b7075dfed00c765d264edcac25ebbfc247f57))
* introduce generic app ([edb7a88](https://github.com/acdh-oeaw/apis-core-rdf/commit/edb7a884f6afe3542d27c6c749f8091a47d8ad64)), closes [#509](https://github.com/acdh-oeaw/apis-core-rdf/issues/509)


### Bug Fixes

* **apis_entities:** drop TempEntityClass ([b08bfb6](https://github.com/acdh-oeaw/apis-core-rdf/commit/b08bfb6f27df35f5f7c8c185ab4e8cb0a9e69791)), closes [#6](https://github.com/acdh-oeaw/apis-core-rdf/issues/6)
* drop collectiontype field from Collection model ([c74f628](https://github.com/acdh-oeaw/apis-core-rdf/commit/c74f6280991fc388c27dc1eadf2f5e7f000be345))


### Code Refactoring

* **apis_vocabularies:** remove apis_vocabularies app ([e89e03d](https://github.com/acdh-oeaw/apis-core-rdf/commit/e89e03dc2e9ce3562bac5c9a7a3b6bf619a23135)), closes [#514](https://github.com/acdh-oeaw/apis-core-rdf/issues/514)

## [0.9.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.9.0...v0.9.1) (2023-12-21)


### Bug Fixes

* deletion of entity objects ([e95e030](https://github.com/acdh-oeaw/apis-core-rdf/commit/e95e030bcb40553e96df6334f121bb5927247bb8)), closes [#485](https://github.com/acdh-oeaw/apis-core-rdf/issues/485)

## [0.9.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.8.1...v0.9.0) (2023-12-19)


### ⚠ BREAKING CHANGES

* drop EntityToProsopogrAPhI API endpoint
* drop `resolve_abbrevations` command
* drop `apis_vocabularies.models.TextType`
* drop `apis_vocabularies.models.LabelType`
* **deps:** django-crispy-forms uses separate template packs since version 2. we depend on crispy-bootstrap4 by default, but projects have to add `crispy_bootstrap4` to the INSTALLED_APPS themselves.
* **apis_labels:** APIS projects will have to remove `apis_core.apis_labels` from their settings `INSTALLED_APPS`

### Features

* **apis_labels:** drop apis_labels ([0c44287](https://github.com/acdh-oeaw/apis-core-rdf/commit/0c44287eac678f40a24c98ffe8b7efb053487db4)), closes [#15](https://github.com/acdh-oeaw/apis-core-rdf/issues/15)
* improve listview pagination ([13088b6](https://github.com/acdh-oeaw/apis-core-rdf/commit/13088b62ffe62ac12599bf91d80c114f3a735f78)), closes [#416](https://github.com/acdh-oeaw/apis-core-rdf/issues/416)


### Bug Fixes

* allow `dumpdata` API access for all authenticated users ([a2ffbfd](https://github.com/acdh-oeaw/apis-core-rdf/commit/a2ffbfd1f7fa96018c79894b3e072f66df8301e2))


### Miscellaneous Chores

* **deps:** add crispy-bootstrap4 as dependency ([759e0c6](https://github.com/acdh-oeaw/apis-core-rdf/commit/759e0c60143b854b706c226293a3c64fd19bab65))


### Code Refactoring

* drop `apis_vocabularies.models.LabelType` ([d690d93](https://github.com/acdh-oeaw/apis-core-rdf/commit/d690d9313805f1f1d582b1689bea2dfa1d9b64c1)), closes [#498](https://github.com/acdh-oeaw/apis-core-rdf/issues/498)
* drop `apis_vocabularies.models.TextType` ([22562cb](https://github.com/acdh-oeaw/apis-core-rdf/commit/22562cbefa82a9aeca94c32e2b2c4b9cfa33fe84)), closes [#499](https://github.com/acdh-oeaw/apis-core-rdf/issues/499)
* drop `resolve_abbrevations` command ([7c3edd8](https://github.com/acdh-oeaw/apis-core-rdf/commit/7c3edd810be7fa6f12c40766dc292d0985fb81ea)), closes [#501](https://github.com/acdh-oeaw/apis-core-rdf/issues/501)
* drop EntityToProsopogrAPhI API endpoint ([0448fec](https://github.com/acdh-oeaw/apis-core-rdf/commit/0448fec6fa715a195dadfc60ec415f4ca64099c3))

## [0.8.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.8.0...v0.8.1) (2023-12-14)


### Bug Fixes

* checks if collections exist in merge function ([f9c5d6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/f9c5d6d14fdc9329a58dfc147db732e05f3bb7ee)), closes [#492](https://github.com/acdh-oeaw/apis-core-rdf/issues/492)

## [0.8.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.7.1...v0.8.0) (2023-12-13)


### ⚠ BREAKING CHANGES

* APIS projects will have to remove the `custom_context_processors` from the list of used `context_processors`
* **apis_entites:** any template in your ontology that inherits from the person_detail_generic template needs to point to the detail_generic template instead

### Features

* **apis_entites:** remove person detail template ([75753d4](https://github.com/acdh-oeaw/apis-core-rdf/commit/75753d49dae4dd2850754fcc3afb44dcd110f80b)), closes [#397](https://github.com/acdh-oeaw/apis-core-rdf/issues/397)
* implement dumpdata view and admin command ([9115fc9](https://github.com/acdh-oeaw/apis-core-rdf/commit/9115fc96bd616e3a0f0d2a5d1fc9b18330fee836)), closes [#273](https://github.com/acdh-oeaw/apis-core-rdf/issues/273)
* let projects override entities forms using classes ([14a2489](https://github.com/acdh-oeaw/apis-core-rdf/commit/14a24898a19fd41e441533d280f02ed16858ac9a))


### Bug Fixes

* drop meta_fields from forms ([378d162](https://github.com/acdh-oeaw/apis-core-rdf/commit/378d1622ac10e938c02f0c411ca06a353b14ff61)), closes [#475](https://github.com/acdh-oeaw/apis-core-rdf/issues/475)
* drop unused code block ([a8488f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8488f383458eee8ec02fa60e347195365e8509f))
* drop unused custom context processors ([5b2bfd6](https://github.com/acdh-oeaw/apis-core-rdf/commit/5b2bfd6de18e074edcc52282943e054d06e19f39))
* link to delete view in entity edit template ([5503a6d](https://github.com/acdh-oeaw/apis-core-rdf/commit/5503a6dbbf89baf3fd6fa3fd7a379136cc3b960e)), closes [#437](https://github.com/acdh-oeaw/apis-core-rdf/issues/437)
* provide a fallback template if basetemplate is not set ([2ee69ce](https://github.com/acdh-oeaw/apis-core-rdf/commit/2ee69ce6b3402b5e598805d0f52155ddfcd919f3))


### Documentation

* drop PyYAML from dependency list, add apis-override-select2js ([087ed95](https://github.com/acdh-oeaw/apis-core-rdf/commit/087ed957070a37cea4157aaf964f2e44c2294c8e))


### Code Refactoring

* drop custom_context_processors ([c3d7155](https://github.com/acdh-oeaw/apis-core-rdf/commit/c3d7155c0756a8f58470e20a3474c7acc2ecddac))

## [0.7.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.7.0...v0.7.1) (2023-11-27)


### Bug Fixes

* cleanup generic edit template ([18234e7](https://github.com/acdh-oeaw/apis-core-rdf/commit/18234e710235eacb83b095bc7eb48c70e09de020))
* integrate django.contrib.auth.urls into apis_core.urls ([39a63f4](https://github.com/acdh-oeaw/apis-core-rdf/commit/39a63f40f3000bb68d76f6e550d9657bc77c2ec6)), closes [#426](https://github.com/acdh-oeaw/apis-core-rdf/issues/426)
* override default for JSONField field ([18c05dd](https://github.com/acdh-oeaw/apis-core-rdf/commit/18c05ddcdc93318e6898ca295b30095d1cd6b306))
* rewrite error message ([d560fe8](https://github.com/acdh-oeaw/apis-core-rdf/commit/d560fe815f4322d5265b4ee60cb3fab68854da05))


### Documentation

* add CONTRIBUTING.md ([fe8f46b](https://github.com/acdh-oeaw/apis-core-rdf/commit/fe8f46bb72a1838234df1becffab4bc4208f680d)), closes [#425](https://github.com/acdh-oeaw/apis-core-rdf/issues/425)

## [0.7.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.3...v0.7.0) (2023-11-14)


### ⚠ BREAKING CHANGES

* get rid of additional_serializer

### Features

* allow overriding the entity listview queryset ([0548faa](https://github.com/acdh-oeaw/apis-core-rdf/commit/0548faab7ac1a99266e5b728de00d373d688b76a))
* introduce `get_member_for_entity` helper ([6436f2f](https://github.com/acdh-oeaw/apis-core-rdf/commit/6436f2f15219daf1c423f4426c6531c40720bd7e))


### Bug Fixes

* cleanup entities detail template ([87834b3](https://github.com/acdh-oeaw/apis-core-rdf/commit/87834b3bfde1edbd75648533103ae5ff0d09f6df)), closes [#396](https://github.com/acdh-oeaw/apis-core-rdf/issues/396)
* don't expect entities to have {start|end}_date_written fields ([4952af2](https://github.com/acdh-oeaw/apis-core-rdf/commit/4952af24727fff9115e84cd9200c9da9af9eaffb)), closes [#405](https://github.com/acdh-oeaw/apis-core-rdf/issues/405)
* drop object_revisions from generic entities edit view ([f08b10c](https://github.com/acdh-oeaw/apis-core-rdf/commit/f08b10c99fccb30a48134e02651c60125aba3fa0))
* improve `get_member_for_entity` helper function ([1f9a1a0](https://github.com/acdh-oeaw/apis-core-rdf/commit/1f9a1a00b368f95000d331ad37fdb9efa6be604c))
* use the new `get_member_for_entity` helper to override table ([caa6f65](https://github.com/acdh-oeaw/apis-core-rdf/commit/caa6f65fa6b1db7a9cd5030d43d32f4b050396ed)), closes [#400](https://github.com/acdh-oeaw/apis-core-rdf/issues/400)


### Documentation

* make install instructions more clear ([e6a4efe](https://github.com/acdh-oeaw/apis-core-rdf/commit/e6a4efe9d243e9eab151ebbd3c85829d4defeb56))


### Code Refactoring

* get rid of additional_serializer ([190e5f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/190e5f3f95b1fd2d7351e6807e27e3acdafd7d80)), closes [#338](https://github.com/acdh-oeaw/apis-core-rdf/issues/338)

## [0.6.3](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.2...v0.6.3) (2023-11-08)


### Bug Fixes

* add apis-override-select2js to dependencies ([697b4e1](https://github.com/acdh-oeaw/apis-core-rdf/commit/697b4e14ebb6313e1b6435984e3b07975817c47e)), closes [#389](https://github.com/acdh-oeaw/apis-core-rdf/issues/389)
* do not expect fields in EntitySerializer ([e4480f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/e4480f3ac1d56a5ff3fa4757cc00e2664d6854a9)), closes [#383](https://github.com/acdh-oeaw/apis-core-rdf/issues/383)
* use RootObject instead of TempEntityClass in GetEntityGeneric ([d03fad5](https://github.com/acdh-oeaw/apis-core-rdf/commit/d03fad57265c4463bbafbf299f2ac2c95b7096a0)), closes [#380](https://github.com/acdh-oeaw/apis-core-rdf/issues/380)


### Documentation

* rearrange installation info and add URL dispatcher info ([7d9fff3](https://github.com/acdh-oeaw/apis-core-rdf/commit/7d9fff3008ec164fb71f43413726f2a07932401e)), closes [#393](https://github.com/acdh-oeaw/apis-core-rdf/issues/393)
* update README, now that apis-override-select2js is a dependency ([f23e9eb](https://github.com/acdh-oeaw/apis-core-rdf/commit/f23e9eb937a6bf74565af2cadce4f1a0591a5c67))

## [0.6.2](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.1...v0.6.2) (2023-10-20)


### Bug Fixes

* add `setuptools` as django-model-utils dependency ([de3a10a](https://github.com/acdh-oeaw/apis-core-rdf/commit/de3a10a71f6a9f25085cbb137b9e1553753aacb4))
* drop `get_child_class()` from AbstractEntity ([e10c661](https://github.com/acdh-oeaw/apis-core-rdf/commit/e10c661ed0bff8e996d9ad2e850aafb909923de3)), closes [#323](https://github.com/acdh-oeaw/apis-core-rdf/issues/323)
* move management command ([f3097ba](https://github.com/acdh-oeaw/apis-core-rdf/commit/f3097baddadf76edf6045a7ceb04a4fe452f688b)), closes [#372](https://github.com/acdh-oeaw/apis-core-rdf/issues/372)
* surround embedding of custom stylesheet with if statement ([039f9d4](https://github.com/acdh-oeaw/apis-core-rdf/commit/039f9d46058b59238b747be9ac16dfa9ca6920b9)), closes [#364](https://github.com/acdh-oeaw/apis-core-rdf/issues/364)
* **ux:** add nav class in template block ([d389856](https://github.com/acdh-oeaw/apis-core-rdf/commit/d3898567810bae976a0286e0b2cd3bd33cce0754))


### Documentation

* drop the poetry add line, as those are all dependencies ([5c61809](https://github.com/acdh-oeaw/apis-core-rdf/commit/5c618098fdd2cc6713aa82826ec6ec0584fc776b))
* start documenting development practices ([025186f](https://github.com/acdh-oeaw/apis-core-rdf/commit/025186f37fcbc6244022e1ed911547da4cd01903))
* update README.md ([8c74d97](https://github.com/acdh-oeaw/apis-core-rdf/commit/8c74d97b6de82022aa157ad5351bbac68ec89921)), closes [#361](https://github.com/acdh-oeaw/apis-core-rdf/issues/361)

## [0.6.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.6.0...v0.6.1) (2023-10-18)


### Bug Fixes

* drop `collections` as default field from entities filter ([05e8ad9](https://github.com/acdh-oeaw/apis-core-rdf/commit/05e8ad9dffd36c6244105fe8a909da9f5dd6be9e)), closes [#354](https://github.com/acdh-oeaw/apis-core-rdf/issues/354)
* instead of pointing to admin, use the user login/logout routes ([a5073db](https://github.com/acdh-oeaw/apis-core-rdf/commit/a5073dbdf7bcecb7f185f9a212f421f4e3dcd316)), closes [#353](https://github.com/acdh-oeaw/apis-core-rdf/issues/353)
* put footer and imprint in separate template blocks ([53b3e10](https://github.com/acdh-oeaw/apis-core-rdf/commit/53b3e10a4f589a73d7163a58ee8bfeab59e879f2)), closes [#345](https://github.com/acdh-oeaw/apis-core-rdf/issues/345)
* readd exclude list of fields in detail view and allow customization ([0bd2446](https://github.com/acdh-oeaw/apis-core-rdf/commit/0bd2446cc590a04c144b819da87f2dcdca69e940))
* use value from model_to_dict instead of getattr ([2e2f5fe](https://github.com/acdh-oeaw/apis-core-rdf/commit/2e2f5fedf5b4494b010fbbf8d58b73702f85869a))

## [0.6.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.5.0...v0.6.0) (2023-10-16)


### ⚠ BREAKING CHANGES

* drop the charts dependency
* if the GenericEntityListFilter was used with the `method` set to one of the included methods, the `method` attribute should now point to `apis_core.utils.filtermethods...`

### Features

* add Property to admin interface ([b11352d](https://github.com/acdh-oeaw/apis-core-rdf/commit/b11352dbfa29ce9f062b626c224a4f62829ffd4f))


### Bug Fixes

* add slash to `shared_url` templatetag ([ff47d2a](https://github.com/acdh-oeaw/apis-core-rdf/commit/ff47d2aadf75cfe6936e5cc3a9f37ad9101f1cb1))
* fixes `merge_with` function expecting TempEntityClass ([e40ecb3](https://github.com/acdh-oeaw/apis-core-rdf/commit/e40ecb32d11ecbc6024173d5f40341a66b6741f2))
* introduce APIS_LIST_LINKS_TO_EDIT variable ([8bc259c](https://github.com/acdh-oeaw/apis-core-rdf/commit/8bc259ca24f03da35ae659a84d38314dc5801a33))
* migrate management commands from `apis-webpage` to `apis-rdf-core` ([09fac5e](https://github.com/acdh-oeaw/apis-core-rdf/commit/09fac5ee9f1bc20d21610326bfa3b74e42b63cf5))
* put function call in separate document.ready function ([dd51f5b](https://github.com/acdh-oeaw/apis-core-rdf/commit/dd51f5b394de077c84eab22913d2db83534459af))
* remove duplicate of `references` attribute in detail view ([a381b02](https://github.com/acdh-oeaw/apis-core-rdf/commit/a381b028cb25637dd638f11c03181a8a9c5dc238))
* the contenttype of the rootobject should not be user editable ([872386e](https://github.com/acdh-oeaw/apis-core-rdf/commit/872386eb35640f1bf13b8716e5ac696422ffc970))


### Documentation

* reference `utils.filtermethods` in configuration ([8b6700d](https://github.com/acdh-oeaw/apis-core-rdf/commit/8b6700d497e42ce3682d063d7f8226c25f441652))


### Code Refactoring

* drop the charts dependency ([c963cd8](https://github.com/acdh-oeaw/apis-core-rdf/commit/c963cd83b7d4e5c32471da6f1d7cb73dbcfe19ff))
* move filtermethods from apis_entities to utils ([5068b49](https://github.com/acdh-oeaw/apis-core-rdf/commit/5068b49633693be0d5054672fe9252b5ee5e0037)), closes [#152](https://github.com/acdh-oeaw/apis-core-rdf/issues/152)

## [0.5.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.4.0...v0.5.0) (2023-10-05)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** drop `Source` model
* drop apis module

### Features

* cleanup the default entity detail and edit view ([8011894](https://github.com/acdh-oeaw/apis-core-rdf/commit/80118942af1b6c3603561f3f0e10cd0837fb6df5))
* introduce new templatetags ([0ce7df4](https://github.com/acdh-oeaw/apis-core-rdf/commit/0ce7df4e34efc31b5b3c80374b70889ffbe7938e)), closes [#293](https://github.com/acdh-oeaw/apis-core-rdf/issues/293)
* put main-menu submenu items in separate blocks ([45e031e](https://github.com/acdh-oeaw/apis-core-rdf/commit/45e031e72efa34362c5bff01830c8f2bb6aed6b4)), closes [#306](https://github.com/acdh-oeaw/apis-core-rdf/issues/306)


### Bug Fixes

* allow overriding the entity form ([f56ef89](https://github.com/acdh-oeaw/apis-core-rdf/commit/f56ef89a571c1eafdbd5b7d09034735f8d30af2e)), closes [#238](https://github.com/acdh-oeaw/apis-core-rdf/issues/238)
* **apis_entities:** only set collection if the attribute exists ([e7be0ec](https://github.com/acdh-oeaw/apis-core-rdf/commit/e7be0ecd3727ecc8db461e1e1636412bfef2ba48)), closes [#313](https://github.com/acdh-oeaw/apis-core-rdf/issues/313)
* build docs without apis module ([b44a706](https://github.com/acdh-oeaw/apis-core-rdf/commit/b44a706e16129b19a463e308619c14a59a42bf7b))
* get rid of text model remains ([8a90be2](https://github.com/acdh-oeaw/apis-core-rdf/commit/8a90be2bf2a6ffcd5ffd6c7af8530cfac9618eb0))
* workaround for entities not inheriting from TempEntityClass ([9ba5778](https://github.com/acdh-oeaw/apis-core-rdf/commit/9ba5778dd3762d9da834cdad277e9f268ac4f17a))


### Code Refactoring

* **apis_metainfo:** drop `Source` model ([e877213](https://github.com/acdh-oeaw/apis-core-rdf/commit/e877213bb431666f9a0cf826433d5196abbfaeb7)), closes [#227](https://github.com/acdh-oeaw/apis-core-rdf/issues/227)
* drop apis module ([cd16eb1](https://github.com/acdh-oeaw/apis-core-rdf/commit/cd16eb19006f1f6a0d2477e32da424026b0a8edb)), closes [#222](https://github.com/acdh-oeaw/apis-core-rdf/issues/222)

## [0.4.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.3.1...v0.4.0) (2023-09-27)


### Features

* replaces feather icons with material-symbols ([1d85d57](https://github.com/acdh-oeaw/apis-core-rdf/commit/1d85d57898594e8bd18b8f30be641a7cd0f97d72))


### Bug Fixes

* **api_routers:** allow to let the `id` field be writable in API ([71f85e6](https://github.com/acdh-oeaw/apis-core-rdf/commit/71f85e66ae077cdd2f527a73e40195c230ea9a4f)), closes [#296](https://github.com/acdh-oeaw/apis-core-rdf/issues/296)
* **apis_entities:** fix reversion for tempentity classes ([cfb1771](https://github.com/acdh-oeaw/apis-core-rdf/commit/cfb17712fc03d36ff2f77d402797d0957da046d3))
* **apis_entities:** only set field attributes for existing fields ([100de8c](https://github.com/acdh-oeaw/apis-core-rdf/commit/100de8c2b62fec99d021e14da8cf58764a4d594c)), closes [#298](https://github.com/acdh-oeaw/apis-core-rdf/issues/298)
* **apis_metainfo:** register the rootobject with reversion ([b7217b9](https://github.com/acdh-oeaw/apis-core-rdf/commit/b7217b9888516b7daa4a69d0191004c627a72207))
* **apis_relations:** fix entity lookup for multi URI entities ([0febd2a](https://github.com/acdh-oeaw/apis-core-rdf/commit/0febd2ab97e8ae0d673d3a13b890d46ee40c01a4)), closes [#221](https://github.com/acdh-oeaw/apis-core-rdf/issues/221)
* **apis_relations:** fix follow of property reveversion registration ([6e4df12](https://github.com/acdh-oeaw/apis-core-rdf/commit/6e4df122688fe4446ced9a52254c68fbfabdbfed))
* LegacyDateMixin get dates from DateParser datetimes ([78215e4](https://github.com/acdh-oeaw/apis-core-rdf/commit/78215e4ba0e69b1ad4b8b9dce7c5899ac18e6a70)), closes [#295](https://github.com/acdh-oeaw/apis-core-rdf/issues/295)
* use empty dict as fallback for PROJECT_DEFAULT_MD ([8aa5394](https://github.com/acdh-oeaw/apis-core-rdf/commit/8aa53943a3202194f15302bf42b14aae27d9d053))

## [0.3.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.3.0...v0.3.1) (2023-09-13)


### Bug Fixes

* add migrations forgotten in 063412f ([7fd93f3](https://github.com/acdh-oeaw/apis-core-rdf/commit/7fd93f353df7c7852e02a8c6ee1ca697185de37a))

## [0.3.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.2.0...v0.3.0) (2023-09-13)


### ⚠ BREAKING CHANGES

* **apis_entities, apis_metainfo:** drop texts
* **apis_metainfo:** cleanup menu block in base template

### Features

* **apis_entities:** enclose the relations listing in a relations block ([f052035](https://github.com/acdh-oeaw/apis-core-rdf/commit/f052035c8b582cc5b9536b635cd8dc965c2b589d))
* **apis_metainfo:** cleanup menu block in base template ([8f5943b](https://github.com/acdh-oeaw/apis-core-rdf/commit/8f5943b45248f10afcddc601cf2ec0f93a350344))
* **core:** add userlogin-menu block to `base.html` ([7bc4a29](https://github.com/acdh-oeaw/apis-core-rdf/commit/7bc4a29b8f3953f30a9e3f678f6e938e4e39023e))
* provide modal block in base template ([86f5d43](https://github.com/acdh-oeaw/apis-core-rdf/commit/86f5d4357908de6af240e523c1cf09db09421e99))


### Bug Fixes

* **apis_entities, apis_metainfo:** drop texts ([063412f](https://github.com/acdh-oeaw/apis-core-rdf/commit/063412fb28bb812325010bae333f19ea3cb7bd8d))
* **apis_metainfo:** drop `browsing/generic_list.html` template ([b5a9f7a](https://github.com/acdh-oeaw/apis-core-rdf/commit/b5a9f7ab8f433e1c957e52c58e4d31f5e3722c03)), closes [#151](https://github.com/acdh-oeaw/apis-core-rdf/issues/151)
* **deps:** loosen Python dependency ([0d37dcc](https://github.com/acdh-oeaw/apis-core-rdf/commit/0d37dcca921ca3ba8e6ce9b21ba2db4be7897e30)), closes [#255](https://github.com/acdh-oeaw/apis-core-rdf/issues/255)

## [0.2.0](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.1.1...v0.2.0) (2023-09-07)


### ⚠ BREAKING CHANGES

* **apis_metainfo:** rename templatetags
* **apis_vis:** drop apis_vis
* **apis_metainfo:** drop UriCandidate

### Features

* **apis_vis:** drop apis_vis ([7e69eb1](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e69eb16cf324fcd8530d0f326a47d1ffc15202c)), closes [#206](https://github.com/acdh-oeaw/apis-core-rdf/issues/206)
* **core:** Introduce LegacyDateMixin ([fe3c205](https://github.com/acdh-oeaw/apis-core-rdf/commit/fe3c20554d5bee21ed44b9cdc43cde9a53d7cdce)), closes [#66](https://github.com/acdh-oeaw/apis-core-rdf/issues/66)
* **utils:** introduce APIS_ENTITIES settings function ([14fa858](https://github.com/acdh-oeaw/apis-core-rdf/commit/14fa858792ef51af03c2229460fe1a4518a82a86))


### Bug Fixes

* **apis_entities,apis_relations:** drop login_url override ([2f3c6a4](https://github.com/acdh-oeaw/apis-core-rdf/commit/2f3c6a40518c43fb915e2a5e858216a59fa22378))
* **apis_entities:** make relations pagination configurable ([164d9dc](https://github.com/acdh-oeaw/apis-core-rdf/commit/164d9dc02b499d35bda13d509e7050c16a8c713b))
* **apis_metainfo:** rename templatetags ([22b8145](https://github.com/acdh-oeaw/apis-core-rdf/commit/22b814555a91b3a0526bc3a153e16c39352ac978)), closes [#163](https://github.com/acdh-oeaw/apis-core-rdf/issues/163)
* show reference button in detail view ([9120ed2](https://github.com/acdh-oeaw/apis-core-rdf/commit/9120ed20a73b54052544c4effc3110b48172bc13))


### Code Refactoring

* **apis_metainfo:** drop UriCandidate ([8de5061](https://github.com/acdh-oeaw/apis-core-rdf/commit/8de5061bbab0bdcae1c1e735320ca6a9ecc37fa2)), closes [#183](https://github.com/acdh-oeaw/apis-core-rdf/issues/183)

## [0.1.1](https://github.com/acdh-oeaw/apis-core-rdf/compare/v0.1.0...v0.1.1) (2023-08-30)


### Bug Fixes

* replace custom duplication logic with signal ([0b1c20d](https://github.com/acdh-oeaw/apis-core-rdf/commit/0b1c20d61aed9d53c6acce90e87e617560f10718))
* use the filter method of the superclass, if it exists ([b96ec9e](https://github.com/acdh-oeaw/apis-core-rdf/commit/b96ec9eb489eaffbec804fa910bf7cb5c47c1fce)), closes [#263](https://github.com/acdh-oeaw/apis-core-rdf/issues/263)

## 0.1.0 (2023-08-28)


### ⚠ BREAKING CHANGES

* **apis_tei:** drop the apis_tei module
* bump Python dependency to >=3.11
* **apis_entities:** this changes the format of the `list_filters` setting of the APIS_ENTITIES setting to a pure dict.
* external projects using functionality from `helper_functions` will have to update their imports.

### Features

* **apis_entities, api_routers:** use access and filter mixins ([47d0cef](https://github.com/acdh-oeaw/apis-core-rdf/commit/47d0cefa500c9ef8b8172aac1c777361da191819))
* **apis_entities,utils:** introduce new tei renderer ([199f2f4](https://github.com/acdh-oeaw/apis-core-rdf/commit/199f2f453dab020f556dcb7c8b6b96e17a96e0d7))
* **apis_entities:** add additional block to generic detail template ([994524c](https://github.com/acdh-oeaw/apis-core-rdf/commit/994524c1e737eb3a2f4a7c7f9b4484baa60ac0d1))
* **apis_entities:** copy fields when merging entities ([66d7c51](https://github.com/acdh-oeaw/apis-core-rdf/commit/66d7c51613ad5de4162da4fbdb8e782b2e9edd10)), closes [#140](https://github.com/acdh-oeaw/apis-core-rdf/issues/140)
* **apis_entities:** filter allowed related types to only allowed ([e374239](https://github.com/acdh-oeaw/apis-core-rdf/commit/e3742395e1e52dea7e0a84e416b9c3b40f720912))
* **apis_entities:** introduce apis_entities.mixins ([5f6c86c](https://github.com/acdh-oeaw/apis-core-rdf/commit/5f6c86c79f483a98d271b8d22819bb861100bb42))
* **apis_entities:** introduce merge_with signal ([844852d](https://github.com/acdh-oeaw/apis-core-rdf/commit/844852dbaf7a18dfb4611d7df6c3ebf25e976033))
* **apis_entities:** let users override the serializer for renderers ([e52fa7f](https://github.com/acdh-oeaw/apis-core-rdf/commit/e52fa7f7045816c36f6822b3326fd5c75b618390))
* **apis_entities:** refactor code and make custom filters possible ([7e0a087](https://github.com/acdh-oeaw/apis-core-rdf/commit/7e0a087e3d00ee6332e6245bc2b61e21f39d2765)), closes [#144](https://github.com/acdh-oeaw/apis-core-rdf/issues/144)
* **apis_metainfo:** introduce an API endpoint for resolving URIs ([461b0eb](https://github.com/acdh-oeaw/apis-core-rdf/commit/461b0eb6b9e15a9a0ce004c8f24154a0d31bc42d))
* **apis_metainfo:** introduce duplication signals ([a54e00e](https://github.com/acdh-oeaw/apis-core-rdf/commit/a54e00e2d4b94229cb4d77c412fdd1bf3ebce2d7))
* **apis_metainfo:** provide a login template ([a8f88f2](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8f88f280ab533d00bf3e9f760ea8749077c7b48)), closes [#210](https://github.com/acdh-oeaw/apis-core-rdf/issues/210)
* **apis_metainfo:** replace fundament with pure bootstrap ([fd7e288](https://github.com/acdh-oeaw/apis-core-rdf/commit/fd7e288efbb77cf7eb9a5ece69cbe5ed8760fd7e)), closes [#180](https://github.com/acdh-oeaw/apis-core-rdf/issues/180)
* **apis_tei:** drop the apis_tei module ([b0bea90](https://github.com/acdh-oeaw/apis-core-rdf/commit/b0bea902cf4507569ab256efaf3082799d6bca9d))
* **core:** Introduce ViewPassesTestMixin and ListViewObjectFilterMixin ([082d798](https://github.com/acdh-oeaw/apis-core-rdf/commit/082d798368fed36aa62fa1da62dd9b860f0816ee))
* implement duplication of RootObject children ([a709639](https://github.com/acdh-oeaw/apis-core-rdf/commit/a70963971896d3d0ba4eb2bc51e68693c47019c9))
* Implement form, view and route for adding URIs ([5a141b6](https://github.com/acdh-oeaw/apis-core-rdf/commit/5a141b6e3d3641f61acd3c9323a577a520f9c084))
* implement new rdf parser ([83ce845](https://github.com/acdh-oeaw/apis-core-rdf/commit/83ce845c73b391f58aadf84033eb396b527d4069))


### Bug Fixes

* add acdh-django-charts dependency ([014da3e](https://github.com/acdh-oeaw/apis-core-rdf/commit/014da3eb1728734f50565fefc5cf998e09767ae1))
* apis_entities: get filter fields from APIS_ENTITIES settings ([a9eb868](https://github.com/acdh-oeaw/apis-core-rdf/commit/a9eb86831c1f180a52b633668b06e09a9afe1c7d))
* apis_entities: template_name should not be prefixed with namespace ([42722f0](https://github.com/acdh-oeaw/apis-core-rdf/commit/42722f04c254da45d683a9cceaf76d4d4b951696))
* apis_entities: use logger instead of an exception ([7f1fcbb](https://github.com/acdh-oeaw/apis-core-rdf/commit/7f1fcbb4d7b13662b9744074877f172ebec3ed1e))
* **apis_entities:** drop django guardian related code and dependency ([8b5f982](https://github.com/acdh-oeaw/apis-core-rdf/commit/8b5f9827bf8047c20de1dad570ca5c41f3817427))
* **apis_entities:** fix transferral of Uris in merge method ([c866a1a](https://github.com/acdh-oeaw/apis-core-rdf/commit/c866a1adda42430650a796e61a3c0b84a55078a3))
* **apis_entities:** remove `merge` column and form ([22f96cf](https://github.com/acdh-oeaw/apis-core-rdf/commit/22f96cf7bd4138f38b32c56542adbf0793429a85)), closes [#168](https://github.com/acdh-oeaw/apis-core-rdf/issues/168)
* **apis_entities:** return uri.root_object instead of uri itself ([abaa1d9](https://github.com/acdh-oeaw/apis-core-rdf/commit/abaa1d96b946e8d843d1ccae443af55717f5fcc2))
* **apis_metainfo:** add zero margin to the usermenu in the navbar ([c35d13b](https://github.com/acdh-oeaw/apis-core-rdf/commit/c35d13bcf026b9946c3ec0eb908b87880a246e02))
* **apis_metainfo:** drop unused api_views module ([d15fa79](https://github.com/acdh-oeaw/apis-core-rdf/commit/d15fa79cd5c9e76612b5bb0aca66ad5186950c19))
* **apis_relations:** fix accidental newline after `if` in template ([b570a8d](https://github.com/acdh-oeaw/apis-core-rdf/commit/b570a8d8101ce8e4ae8a617a01f0924e933cfadb)), closes [#236](https://github.com/acdh-oeaw/apis-core-rdf/issues/236)
* **apis:** show an empty page on `/` instead of an errorpage ([95f97d4](https://github.com/acdh-oeaw/apis-core-rdf/commit/95f97d4153318b92316e2da4f64bc5d99b699bff))
* Changed ContentType.objects.get(model=&lt;MODEL NAME&gt;) to ContentType.objects.get_for_model(<MODEL>) ([7dfa2ac](https://github.com/acdh-oeaw/apis-core-rdf/commit/7dfa2ac1d8ad97584a55f9b5c865e451959971a0))
* cleanup entity_settings vs APIS_SETTINGS ([0bc67a8](https://github.com/acdh-oeaw/apis-core-rdf/commit/0bc67a8771830d0c5c65fd5fda4c0f5d15efa0e6))
* drop legacy RDF parser ([602aebd](https://github.com/acdh-oeaw/apis-core-rdf/commit/602aebdd441ed140cfd58173b0e4a8cc32680371))
* fixes [#117](https://github.com/acdh-oeaw/apis-core-rdf/issues/117) ([8e7a713](https://github.com/acdh-oeaw/apis-core-rdf/commit/8e7a7131c36e227ef98ded51337830cef2b1cdd0))
* harden and enhance Uri model ([d8f26b8](https://github.com/acdh-oeaw/apis-core-rdf/commit/d8f26b833b8255b9ff4049081e761f2b3f9d1af7))
* lowers django version to allow for MariaDB 10.3 ([a8f76f7](https://github.com/acdh-oeaw/apis-core-rdf/commit/a8f76f7b96a292cc4faeb751eb2430bbe4bd9477))
* Set the default_auto_field in all the apps ([69af77f](https://github.com/acdh-oeaw/apis-core-rdf/commit/69af77f23c6208db551040970516882a36ff9a86))
* typo in template ([082ec37](https://github.com/acdh-oeaw/apis-core-rdf/commit/082ec37bd0f5f2f88c8816a647f532f98cfe2df5))
* use the new BASE_TEMPLATE ([ea7936e](https://github.com/acdh-oeaw/apis-core-rdf/commit/ea7936e6266807d88644b5deb05698ffa42257d5))
* **utils:** fix bug and add test case ([a3e9a3a](https://github.com/acdh-oeaw/apis-core-rdf/commit/a3e9a3ae23aa5574307212daaf7814e555670935))
* **utils:** use local files for rdf parser to circument http timeouts ([ce0dd89](https://github.com/acdh-oeaw/apis-core-rdf/commit/ce0dd89bb43327da0034cc51ca3b331fb6450e12)), closes [#174](https://github.com/acdh-oeaw/apis-core-rdf/issues/174)


### Documentation

* Add a workflow that builds and publishes documentation ([bebc4a7](https://github.com/acdh-oeaw/apis-core-rdf/commit/bebc4a76805990eea735288621cdb202acebd6dc)), closes [#67](https://github.com/acdh-oeaw/apis-core-rdf/issues/67)
* Add docs dependencies to pyproject.toml ([912f7a8](https://github.com/acdh-oeaw/apis-core-rdf/commit/912f7a8e60ed21889621ce8f882eb31edefac049))
* add documentation for custom access and list view filter settings ([efa0fea](https://github.com/acdh-oeaw/apis-core-rdf/commit/efa0fea3a78ba7fbc75de5cfbed00352d07254cd))
* add new Makefile and .gitignore ([166f223](https://github.com/acdh-oeaw/apis-core-rdf/commit/166f2238dc325c8cdd75bbe50f03f2fbfca643f5))
* automatically generate module documentation ([6456261](https://github.com/acdh-oeaw/apis-core-rdf/commit/645626179bdb83046ed6f2080353ed23f9ba7d3b))
* Delete stale generated documentation ([1b83caf](https://github.com/acdh-oeaw/apis-core-rdf/commit/1b83caf0d3f07b4e9f7b9a5dd853abbe83c411c6))
* remove stale .doctrees directory ([9582ac2](https://github.com/acdh-oeaw/apis-core-rdf/commit/9582ac292d8eea166a45468868ff687e7f0e27ad))
* Start a glossary ([337ecd5](https://github.com/acdh-oeaw/apis-core-rdf/commit/337ecd5fc06a6b9d5da37038b8c212cfc0fade2f))
* update documentation regarding new entity filters ([f828511](https://github.com/acdh-oeaw/apis-core-rdf/commit/f82851150308ba6bc2a3e7274897fe2f19886ea4))


### Styles

* rename `helper_functions` to `utils` ([0f083d5](https://github.com/acdh-oeaw/apis-core-rdf/commit/0f083d5d17a17b311435b540af0b19368654de20)), closes [#131](https://github.com/acdh-oeaw/apis-core-rdf/issues/131)


### Miscellaneous Chores

* bump Python dependency to &gt;=3.11 ([3a67844](https://github.com/acdh-oeaw/apis-core-rdf/commit/3a67844d357af33e4a344bdb2f21be7d4f00a1ab)), closes [#171](https://github.com/acdh-oeaw/apis-core-rdf/issues/171)
