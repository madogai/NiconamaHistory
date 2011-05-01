python経験者向けプラグインの作り方
==================================

プラグインの概要
----------------

* :doc:`niconama_history.plugin_base.PluginBaseクラス<../niconama_history/plugin_base>` を継承するとプラグインとして認識されます。
* 1つのモジュールには複数のプラグインを含める事ができます。
* プラグインを含んだモジュールをpluginsフォルダ配下に配置する事でプラグインとして認識します。

プラグインの実装方法
--------------------

:doc:`PluginBase<../niconama_history/plugin_base>` のメソッドをオーバーライドしてください。
不要なメソッドをオーバーライドする必要はありません。

Commentクラス
-------------

.. list-table::
   :header-rows: 1

   * - PropertyName
     - Type
   * - communityId
     - Text
   * - liveId
     - Text
   * - userId
     - Text
   * - name
     - Text
   * - message
     - Text
   * - option
     - Text
   * - datetime
     - Text

Comment(DBテーブル)
-------------------

.. list-table::
   :header-rows: 1

   * - ColumnName
     - Type
   * - community_id
     - Text
   * - live_id
     - Text
   * - user_id
     - Text
   * - name
     - Text
   * - message
     - Text
   * - option
     - Text
   * - datetime
     - Text