// Copyright (c) Dataflow Notebook Development Team.
// Distributed under the terms of the BSD-3 License.
/**
 *
 *
 * @module dfgraph
 * @namespace dfgraph
 * @class DfGraph
 */


define([
    'jquery',
    'base/js/namespace',
    './depview.js',
    'notebook/js/celltoolbar',
], function(
    $,
    Jupyter,
    depview,
    celltoolbar
    ) {
    "use strict";

    var DfGraph = function (cells, nodes, uplinks, downlinks, internal_nodes, all_down) {
        /**
         * Constructor
         *
         * The DfGraph which contains all the link information between cells
         *
         * Parameters:
         *  cells: A list of all cells in the notebook
         *  nodes: A list of nodes in the notebook
         *      The nodes don't have to be set at creation time,
         *      they will be set as an empty list and will be set on later execution.
         *  links: A list of all the links between dependencies
         *  ie Out[bbb] relies on Out[aaa]
         *  each link is a pair of keys {'upstream':'aaa','downstream':'bbb'}
         *  internal_nodes: A dictionary of all internal name nodes for each cell
         *
         */
        this.was_changed = false;
        this.cells = cells || [];
        this.nodes = nodes || [];
        this.uplinks = uplinks || {};
        this.downlinks = downlinks || {};
        this.internal_nodes = internal_nodes || {};

        //Cache downstream lists
        this.downstream_lists = all_down || {};
        this.upstream_list = {};
        this.depview = new depview.DepView(this);


    };

    DfGraph.prototype = Object.create(DfGraph.prototype);


    /** @method update_graph */
    DfGraph.prototype.update_graph = function(cells,nodes,uplinks,downlinks,uuid,all_ups,internal_nodes){
        var that = this;
        if(that.depview.is_open === false){
            that.was_changed = true;
        }
        that.cells = cells;
        that.nodes[uuid] = nodes || [];
        if(uuid in that.uplinks){
            Object.keys(that.uplinks[uuid]).forEach(function (uplink) {
                that.downlinks[uplink] = [];
            });
        }
        that.uplinks[uuid] = uplinks;
        that.downlinks[uuid] = downlinks || [];
        that.internal_nodes[uuid] = internal_nodes;
        that.update_dep_lists(all_ups,uuid);
        celltoolbar.CellToolbar.rebuild_all();
    };

    /** @method removes a cell entirely from the graph **/
    DfGraph.prototype.remove_cell = function(uuid){
        var that = this;
        var cell_index = that.cells.indexOf(uuid);
        if(cell_index > -1){
          that.cells.splice(cell_index,1);
          delete that.nodes[uuid];
          delete that.internal_nodes[uuid];
          delete that.downstream_lists[uuid];
          (that.downlinks[uuid] || []).forEach(function (down) {
              if(down in that.uplinks && uuid in that.uplinks[down]){
                  delete (that.uplinks[down])[uuid];
              }
          });
          delete that.downlinks[uuid];
          if(uuid in that.uplinks) {
              var uplinks = Object.keys(that.uplinks[uuid]);
                  uplinks.forEach(function (up) {
                      var idx = that.downlinks[up].indexOf(uuid);
                      that.downlinks[up].splice(idx,1);
                  });
          }
          delete that.uplinks[uuid];
          if(uuid in that.upstream_list){
              var all_ups = that.upstream_list[uuid].slice(0);
              delete that.upstream_list[uuid];
              all_ups.forEach(function (up) {
                      //Better to just invalidate the cached list so you don't have to worry about downstreams too
                      delete that.downstream_lists[up];
              });
          }
        }
    };

    /** @method set_internal_nodes */
    DfGraph.prototype.set_internal_nodes = function(uuid,internal_nodes){
        this.internal_nodes[uuid] = internal_nodes;
    };

    /** @method this is a set addition method for dependencies */
    Array.prototype.setadd = function(item) {
        var that = this;
        if(that.indexOf(item) < 0){
            that.push(item);
        }
    };

    /** @method update_graph */
    DfGraph.prototype.update_dep_view = function() {
    var depview = this.depview;
    if(depview.is_open){
        var g = depview.create_node_relations(depview.globaldf, depview.globalselect);
        depview.create_graph(g);
    }
    };

    /** @method recursively yield all downstream deps */
    DfGraph.prototype.all_downstream = function(uuid){
        var that = this;
        var visited = [];
        var res = [];
        var downlinks = (this.downlinks[uuid] || []).slice(0);
        while(downlinks.length > 0){
            var cid = downlinks.pop();
            visited.setadd(cid);
            res.setadd(cid);
            if(cid in that.downstream_lists)
            {
                that.downstream_lists[cid].forEach(function (pid) {
                    res.setadd(pid);
                    visited.setadd(pid);
                });
            }
            else{
                if(cid in that.downlinks) {
                    that.downlinks[cid].forEach(function (pid) {
                        if (visited.indexOf(pid) < 0) {
                            downlinks.push(pid);
                        }
                    })
                }
                else{
                    var idx = res.indexOf(cid);
                    res.splice(idx,1);
                }
            }
        }
        that.downstream_lists[uuid] = res;
        return res;
    };

    DfGraph.prototype.all_upstream_cell_ids = function(cid) {
        var that = this;
        var uplinks = this.get_imm_upstreams(cid);
        var all_cids = [];
        while (uplinks.length > 0) {
            var up_cid = uplinks.pop();
            all_cids.setadd(up_cid);
            uplinks = uplinks.concat(this.get_imm_upstreams(up_cid));
        }
        return all_cids;
    };

    /** @method updates all downstream links with downstream updates passed from kernel */
    DfGraph.prototype.update_down_links = function (downupdates) {
        var that = this;
        downupdates.forEach(function (t) {
            var uuid = t['key'].substr(0, 6);
            if(Jupyter.notebook.has_id(uuid) && t.data){
                that.downlinks[uuid] = t['data'];
            }
        });
        that.downstream_lists = {};
    };

    /** @method update_dep_lists */
    DfGraph.prototype.update_dep_lists = function(all_ups,uuid){
        var that = this;
    //     var cell = Jupyter.notebook.get_code_cell(uuid);
    //
    //     if(cell.last_msg_id){
    //         cell.clear_df_info();
    //     }
    //
    //     if(that.downlinks[uuid].length > 0){
    //         cell.update_df_list(cell,that.all_downstream(uuid),'downstream');
    //     }
    //
        if(all_ups.length > 0){
           that.upstream_list[uuid] = all_ups;
    //        cell.update_df_list(cell,all_ups,'upstream');
        }
    };

    /** @method returns the cached all upstreams for a cell with a given uuid */
    DfGraph.prototype.get_all_upstreams = function (uuid) {
        return this.upstream_list[uuid];
    };

    /** @method returns upstreams for a cell with a given uuid */
    DfGraph.prototype.get_upstreams = function(uuid){
        var that = this;
        return Object.keys(that.uplinks[uuid] || []).reduce(function (arr,uplink) {
           var links = that.uplinks[uuid][uplink].map(function (item){
               return uplink === item ? item : uplink+item;}) || [];
            return arr.concat(links);
        },[]);
    };

    /** @method returns single cell based upstreams for a cell with a given uuid */
    DfGraph.prototype.get_imm_upstreams = function(uuid){
        if (uuid in this.uplinks) {
            return Object.keys(this.uplinks[uuid]);
        }
        return [];
    };

    DfGraph.prototype.get_imm_upstream_names = function(uuid) {
        var arr = [];
        var that = this;
        this.get_imm_upstreams(uuid).forEach(function(up_uuid) {
            Array.prototype.push.apply(arr, that.uplinks[uuid][up_uuid]);
        });
        return arr;
    };

    DfGraph.prototype.get_imm_upstream_pairs = function(uuid) {
        var arr = [];
        var that = this;
        this.get_imm_upstreams(uuid).forEach(function(up_uuid) {
            Array.prototype.push.apply(arr, that.uplinks[uuid][up_uuid].map(function(v) { return [v, up_uuid];}));
        });
        return arr;
    };


    /** @method returns downstreams for a cell with a given uuid */
    DfGraph.prototype.get_downstreams = function (uuid) {
        return this.downlinks[uuid];
    };

    /** @method returns the cached all upstreams for a cell with a given uuid */
    DfGraph.prototype.get_internal_nodes = function (uuid) {
        return this.internal_nodes[uuid] || [];
    };

    /** @method returns all nodes for a cell*/
    DfGraph.prototype.get_nodes = function(uuid){
        var that = this;
        if (uuid in that.nodes) {
            if ((that.nodes[uuid] || []).length > 0) {
                return that.nodes[uuid];
            }
        }
        return [];
    };

    /** @method returns all cells on kernel side*/
    DfGraph.prototype.get_cells = function(){
        return this.cells;
    };


    return {'DfGraph': DfGraph};
});