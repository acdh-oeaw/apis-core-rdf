# Changelog

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
