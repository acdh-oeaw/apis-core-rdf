# Changelog

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
