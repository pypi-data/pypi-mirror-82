webpackJsonp([39],{0:function(e,s,t){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}var i=t(80),a=_interopRequireDefault(i),o=t(5),n=_interopRequireDefault(o),r=t(31),d=_interopRequireDefault(r);t(965);var c=t(338),u=_interopRequireDefault(c),l=t(343),p=_interopRequireDefault(l);new d.default({mixins:[a.default],components:{ShareButton:u.default,DiscussionThreads:p.default},ready:function(){n.default.debug("Post page ready")}})},70:function(e,s,t){var i,a;i=t(307),a=t(330),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},296:function(e,s){"use strict";Object.defineProperty(s,"__esModule",{value:!0});var t=2;s.default={name:"pagination-widget",props:{p:Object},computed:{start:function(){return this.p?this.p.page<=t?1:this.p.page-t:-1},end:function(){return this.p?this.p.page+t>this.p.pages?this.p.pages:this.p.page+t:-1},range:function(){var e=this;return isNaN(this.start)||isNaN(this.end)||this.start>=this.end?[]:Array.apply(0,Array(this.end+1-this.start)).map(function(s,t){return t+e.start})}}}},297:function(e,s){e.exports=' <ul class="pagination pagination-sm no-margin" v-show="p && p.pages > 1"> <li :class="{ \'disabled\': !p || p.page == 1 }"> <a :title="_(\'First page\')" class=pointer @click=p.go_to_page(1)> &laquo; </a> </li> <li :class="{ \'disabled\': !p || p.page == 1 }"> <a :title="_(\'Previous page\')" class=pointer @click=p.previousPage()> &lsaquo; </a> </li> <li v-for="current in range" :class="{ \'active\': current == p.page }"> <a @click=p.go_to_page(current) class=pointer>{{ current }}</a> </li> <li :class="{ \'disabled\': !p || p.page == p.pages }"> <a :title="_(\'Next page\')" class=pointer @click=p.nextPage()> &rsaquo; </a> </li> <li :class="{ \'disabled\': !p || p.page == p.pages }"> <a :title="_(\'Last page\')" class=pointer @click=p.go_to_page(p.pages)> &raquo; </a> </li> </ul> '},298:function(e,s,t){var i,a;i=t(296),a=t(297),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},307:function(e,s){"use strict";Object.defineProperty(s,"__esModule",{value:!0});var t=52;s.default={props:{user:Object,size:{type:Number,default:t}}}},308:function(e,s,t){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(s,"__esModule",{value:!0});var i=t(52),a=(_interopRequireDefault(i),t(75)),o=_interopRequireDefault(a);s.default={props:{title:{type:String,required:!0},url:{type:String,required:!0}},filters:{encode:encodeURIComponent},methods:{click:function(){o.default.publish("SHARE"),this.$refs.popover.show=!1}}}},309:function(e,s,t){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(s,"__esModule",{value:!0});var i=t(15),a=_interopRequireDefault(i),o=t(70),n=_interopRequireDefault(o);s.default={components:{Avatar:n.default},props:{message:Object,discussion:String,index:Number},methods:{formatDate:function(e){return(0,a.default)(e).format("LL")}}}},310:function(e,s,t){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(s,"__esModule",{value:!0});var i=t(5),a=_interopRequireDefault(i);s.default={props:{subjectId:String,subjectClass:String,position:Number},data:function(){return{sending:!1,title:"",comment:""}},methods:{prefill:function(e,s){s=s||"",this.comment=s,this.title=e||"",e?(this.$els.textarea.setSelectionRange(s.length,s.length),this.$els.textarea.focus()):this.$els.title.focus()},submit:function(){var e=this,s={title:this.title,comment:this.comment,subject:{id:this.subjectId,class:this.subjectClass}};this.sending=!0,this.$api.post("discussions/",s).then(function(s){e.$dispatch("discussion:created",s),e.title="",e.comment="",e.sending=!1,document.location.href="#discussion-"+s.id}).catch(function(s){var t=e._("An error occured while submitting your comment");e.$dispatch("notify:error",t),a.default.error(s),e.sending=!1})}}}},311:function(e,s,t){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(s,"__esModule",{value:!0});var i=t(5),a=_interopRequireDefault(i);s.default={props:{discussionId:String},data:function(){return{sending:!1,comment:"",id:"new-comment-"+this.discussionId}},methods:{prefill:function(e){e=e||"",this.comment=e,this.$els.textarea.setSelectionRange(e.length,e.length),this.$els.textarea.focus()},submit:function(){var e=this;this.sending=!0,this.$api.post("discussions/"+this.discussionId+"/",{comment:this.comment}).then(function(s){e.$dispatch("discussion:updated",s),e.comment="",e.sending=!1,document.location.href="#discussion-"+e.discussionId+"-"+(s.discussion.length-1)}).catch(function(s){var t=e._("An error occured while submitting your comment");e.$dispatch("notify.error",t),a.default.error(s),e.sending=!1})}}}},312:function(e,s,t){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(s,"__esModule",{value:!0});var i=t(12),a=_interopRequireDefault(i),o=t(339),n=_interopRequireDefault(o),r=t(341),d=_interopRequireDefault(r),c=t(15),u=_interopRequireDefault(c),l=t(70);_interopRequireDefault(l);s.default={components:{ThreadMessage:n.default,ThreadForm:d.default},props:{discussion:Object,position:Number},data:function(){return{detailed:!0,formDisplayed:!1,currentUser:a.default.user}},events:{"discussion:updated":function(e){return this.hideForm(),!0}},computed:{discussionIdAttr:function(){return"discussion-"+this.discussion.id},createdDate:function(){return(0,u.default)(this.discussion.created).format("LL")},closedDate:function(){return(0,u.default)(this.discussion.closed).format("LL")}},methods:{toggleDiscussions:function(){this.detailed=!this.detailed},displayForm:function(){this.$auth(this._("You need to be logged in to comment.")),this.formDisplayed=!0,this.detailed=!0},hideForm:function(){this.formDisplayed=!1},start:function(e){var s=this;this.displayForm(),this.$nextTick(function(){s.$els.form&&s.$refs.form&&(s.$scrollTo(s.$els.form),s.$refs.form.prefill(e))})},focus:function(e){var s=this;this.detailed=!0,e?this.$nextTick(function(){s.$scrollTo("#"+s.discussionIdAttr+"-"+e)}):this.$scrollTo(this)}}}},313:function(e,s,t){"use strict";function _interopRequireDefault(e){return e&&e.__esModule?e:{default:e}}Object.defineProperty(s,"__esModule",{value:!0});var i=t(79),a=_interopRequireDefault(i),o=t(123),n=_interopRequireDefault(o),r=t(12),d=_interopRequireDefault(r),c=t(70),u=_interopRequireDefault(c),l=t(342),p=_interopRequireDefault(l),f=t(340),m=_interopRequireDefault(f),g=t(298),b=_interopRequireDefault(g),h=t(5),v=_interopRequireDefault(h),A=/^#discussion-([0-9a-f]{24})$/,_=/^#discussion-([0-9a-f]{24})-(\d+)$/,x=/^#discussion-([0-9a-f]{24})-new-comment$/;s.default={components:{Avatar:u.default,DiscussionThread:p.default,ThreadFormCreate:m.default,PaginationWidget:b.default},data:function(){return{discussions:[],p:{},loading:!0,formDisplayed:!1,currentUser:d.default.user}},props:{subjectId:String,subjectClass:String},events:{"discussion:created":function(e){var s=this;this.hideForm(),this.discussions.unshift(e),this.$nextTick(function(){var t=s.threadFor(e.id);t.detailed=!0,s.$scrollTo(t)})},"discussion:updated":function(e){var s=this.discussions.indexOf(this.discussions.find(function(s){return s.id==e.id}));this.discussions.$set(s,e)}},ready:function(){this.go_to_page(1)},methods:{displayForm:function(){this.$auth(this._("You need to be logged in to start a discussion.")),this.formDisplayed=!0},hideForm:function(){this.formDisplayed=!1},start:function(e,s){var t=this;this.displayForm(),this.$nextTick(function(){t.$els.form&&t.$refs.form&&(t.$scrollTo(t.$els.form),t.$refs.form.prefill(e,s))})},threadFor:function(e){return this.$refs.threads.find(function(s){return s.discussion.id==e})},sortBy:function(e){"created"===e?this.discussions.sort(function(e,s){return new Date(s.created)-new Date(e.created)}):"response"===e&&this.discussions.sort(function(e,s){return new Date(s.discussion.slice(-1)[0].posted_on)-new Date(e.discussion.slice(-1)[0].posted_on)})},jumpToHash:function(e){if("#discussion-create"===e)this.start();else if(A.test(e)){var s=e.match(A),t=(0,n.default)(s,2),i=t[1];this.threadFor(i).focus()}else if(_.test(e)){var a=e.match(_),o=(0,n.default)(a,3),r=o[1],d=o[2];this.threadFor(r).focus(d)}else if(x.test(e)){var c=e.match(x),u=(0,n.default)(c,2),l=u[1];this.threadFor(l).start()}},go_to_page:function(e){var s=this;this.loading=!0,this.$api.get("discussions/",{for:this.subjectId,page:e}).then(function(e){s.loading=!1,s.discussions=e.data;var t=Math.ceil(e.total/e.page_size),i=function(){e.page>1&&s.go_to_page(e.page-1)},o=function(){e.page<e.pages&&s.go_to_page(e.page+1)},n={page:e.page,page_size:e.page_size,pages:t,go_to_page:s.go_to_page,previousPage:i,nextPage:o};s.p=(0,a.default)({},s.p,n),document.location.hash&&s.$nextTick(function(){s.jumpToHash(document.location.hash)})}).catch(v.default.error.bind(v.default))}}}},324:function(e,s,t){s=e.exports=t(8)(),s.push([e.id,"","",{version:3,sources:[],names:[],mappings:"",file:"share.vue",sourceRoot:"webpack://"}])},325:function(e,s,t){s=e.exports=t(8)(),s.push([e.id,".discussion-message{display:flex;flex-direction:row;padding-top:1.25em}.discussion-message>.avatar{margin-right:1em;flex-basis:auto}.discussion-message .message-content{display:flex;flex-direction:column;min-width:0;flex-grow:1}.discussion-message .message-content .message-header{display:flex;flex:0 0 auto;margin-bottom:.5em}.discussion-message .message-content .message-header .author{flex:1 0 auto;font-weight:700}.discussion-message .message-content .message-header .posted_on{flex:0 0 auto;text-align:right}.discussion-message .message-content .message-header .posted_on .fa{margin-left:5px}.discussion-message .message-content .body{flex:1 0 auto}.discussion-message .message-content .body a,.discussion-message .message-content .body code{word-wrap:break-word;word-break:break-all}.discussion-message .message-content .body pre code{word-wrap:normal;word-break:normal}@media only screen and (max-width:480px){.avatar img{width:32px;height:32px}}","",{version:3,sources:["/./js/components/discussions/message.vue"],names:[],mappings:"AAAA,oBAAoB,aAAa,mBAAmB,kBAAkB,CAAC,4BAA4B,iBAAiB,eAAe,CAAC,qCAAqC,aAAa,sBAAsB,YAAY,WAAW,CAAC,qDAAqD,aAAa,cAAc,kBAAkB,CAAC,6DAA6D,cAAc,eAAgB,CAAC,gEAAgE,cAAc,gBAAgB,CAAC,oEAAoE,eAAe,CAAC,2CAA2C,aAAa,CAAC,6FAA6F,qBAAqB,oBAAoB,CAAC,oDAAoD,iBAAiB,iBAAiB,CAAC,yCAAyC,YAAY,WAAW,WAAW,CAAC,CAAC",file:"message.vue",sourcesContent:[".discussion-message{display:flex;flex-direction:row;padding-top:1.25em}.discussion-message>.avatar{margin-right:1em;flex-basis:auto}.discussion-message .message-content{display:flex;flex-direction:column;min-width:0;flex-grow:1}.discussion-message .message-content .message-header{display:flex;flex:0 0 auto;margin-bottom:.5em}.discussion-message .message-content .message-header .author{flex:1 0 auto;font-weight:bold}.discussion-message .message-content .message-header .posted_on{flex:0 0 auto;text-align:right}.discussion-message .message-content .message-header .posted_on .fa{margin-left:5px}.discussion-message .message-content .body{flex:1 0 auto}.discussion-message .message-content .body a,.discussion-message .message-content .body code{word-wrap:break-word;word-break:break-all}.discussion-message .message-content .body pre code{word-wrap:normal;word-break:normal}@media only screen and (max-width:480px){.avatar img{width:32px;height:32px}}"],sourceRoot:"webpack://"}])},326:function(e,s,t){s=e.exports=t(8)(),s.push([e.id,".panel .panel-heading[_v-67a4da23]{padding:10px 15px;cursor:pointer}.read-more[_v-67a4da23]{text-align:center;cursor:pointer}.add-comment[_v-67a4da23]{padding:10px 15px}.add-comment>button.btn[_v-67a4da23]{margin:0 auto;display:block}","",{version:3,sources:["/./js/components/discussions/thread.vue"],names:[],mappings:"AAAA,mCAAmC,kBAAkB,cAAc,CAAC,wBAAwB,kBAAkB,cAAc,CAAC,0BAA0B,iBAAiB,CAAC,qCAAqC,cAAc,aAAa,CAAC",file:"thread.vue",sourcesContent:[".panel .panel-heading[_v-67a4da23]{padding:10px 15px;cursor:pointer}.read-more[_v-67a4da23]{text-align:center;cursor:pointer}.add-comment[_v-67a4da23]{padding:10px 15px}.add-comment>button.btn[_v-67a4da23]{margin:0 auto;display:block}"],sourceRoot:"webpack://"}])},327:function(e,s,t){s=e.exports=t(8)(),s.push([e.id,".control[_v-debbe940]{display:flex;flex-direction:row}.control .pagination[_v-debbe940]{margin-top:0;flex-grow:1}.loading[_v-debbe940]{margin:2em;text-align:center}.discussion-card.add[_v-debbe940]{cursor:pointer}.discussion-card.add .card-logo[_v-debbe940]{background-color:#eee;font-size:2em;display:flex;justify-content:center;align-items:center;height:60px}.discussion-card.add .card-body[_v-debbe940]{min-height:auto;justify-content:left}.discussion-card.add .card-body h4[_v-debbe940]{margin-bottom:0}.create>div[_v-debbe940]:first-child{display:flex;flex-direction:row}.create>div:first-child>div[_v-debbe940]:nth-child(3){padding:0 1em}.create>div:first-child .control[_v-debbe940]{text-align:right;width:4em;order:3}.create>div:first-child .control a[_v-debbe940]:hover{cursor:pointer}.list-group-form[_v-debbe940]{height:inherit}.list-group-form form[_v-debbe940]{padding:1em}","",{version:3,sources:["/./js/components/discussions/threads.vue"],names:[],mappings:"AAAA,sBAAsB,aAAa,kBAAkB,CAAC,kCAAkC,aAAa,WAAW,CAAC,sBAAsB,WAAW,iBAAiB,CAAC,kCAAkC,cAAc,CAAC,6CAA6C,sBAAyB,cAAc,aAAa,uBAAuB,mBAAmB,WAAW,CAAC,6CAA6C,gBAAgB,oBAAoB,CAAC,gDAAgD,eAAe,CAAC,qCAAqC,aAAa,kBAAkB,CAAC,sDAAsD,aAAa,CAAC,8CAA8C,iBAAiB,UAAU,OAAO,CAAC,sDAAsD,cAAc,CAAC,8BAA8B,cAAc,CAAC,mCAAmC,WAAW,CAAC",file:"threads.vue",sourcesContent:[".control[_v-debbe940]{display:flex;flex-direction:row}.control .pagination[_v-debbe940]{margin-top:0;flex-grow:1}.loading[_v-debbe940]{margin:2em;text-align:center}.discussion-card.add[_v-debbe940]{cursor:pointer}.discussion-card.add .card-logo[_v-debbe940]{background-color:#eeeeee;font-size:2em;display:flex;justify-content:center;align-items:center;height:60px}.discussion-card.add .card-body[_v-debbe940]{min-height:auto;justify-content:left}.discussion-card.add .card-body h4[_v-debbe940]{margin-bottom:0}.create>div[_v-debbe940]:first-child{display:flex;flex-direction:row}.create>div:first-child>div[_v-debbe940]:nth-child(3){padding:0 1em}.create>div:first-child .control[_v-debbe940]{text-align:right;width:4em;order:3}.create>div:first-child .control a[_v-debbe940]:hover{cursor:pointer}.list-group-form[_v-debbe940]{height:inherit}.list-group-form form[_v-debbe940]{padding:1em}"],sourceRoot:"webpack://"}])},330:function(e,s){e.exports=' <a class=avatar :href=user.url :title="user | display"> <img class=avatar :src="user | avatar_url size" :alt="user | display" :width=size :height=size> </a> '},331:function(e,s){e.exports=' <button type=button class="btn btn-primary btn-share" :title="_(\'Share\')" v-tooltip v-popover popover-large :popover-title="_(\'Share\')"> <span class="fa fa-share-alt"></span> <div class="btn-group btn-group-lg" data-popover-content> <a class="btn btn-link" title=Google+ @click=click href="https://plus.google.com/share?url={{url|encode}}" target=_blank> <span class="fa fa-2x fa-google-plus"></span> </a> <a class="btn btn-link" title=Twitter @click=click href="https://twitter.com/home?status={{title|encode}}%20-%20{{url|encode}}" target=_blank> <span class="fa fa-2x fa-twitter"></span> </a> <a class="btn btn-link" title=Facebook @click=click href="https://www.facebook.com/sharer/sharer.php?u={{url|encode}}" target=_blank> <span class="fa fa-2x fa-facebook"></span> </a> <a class="btn btn-link" title=LinkedIn @click=click href="https://www.linkedin.com/shareArticle?mini=true&url={{url|encode}}&title={{title|encode}}" target=_blank> <span class="fa fa-2x fa-linkedin"></span> </a> </div> </button> '},332:function(e,s){e.exports=' <div class=discussion-message> <div class=avatar> <a href="{{ message.posted_by.page }}"><avatar :user=message.posted_by></avatar></a> </div> <div class=message-content> <div class=message-header> <div class=author> <a href="{{ message.posted_by.page }}">{{ message.posted_by | display }}</a> </div> <div class=posted_on> {{ formatDate(message.posted_on) }} <a href="#{{ discussion }}-{{ index }}"><span class="fa fa-link"></span></a> </div> </div> <div class=body> {{{ message.content | markdown }}} </div> </div> </div> '},333:function(e,s){e.exports=" <form role=form class=animated @submit.prevent=submit> <div class=form-group> <label for=title-new-discussion>{{ _('Title') }}</label> <input v-el:title type=text id=title-new-discussion v-model=title class=form-control required/> <label for=comment-new-discussion>{{ _('Comment') }}</label> <textarea v-el:textarea id=comment-new-discussion v-model=comment class=form-control rows=3 required></textarea> </div> <button type=submit :disabled=\"this.sending || !this.title || !this.comment\" class=\"btn btn-primary btn-block submit-new-discussion\"> {{ _('Start a discussion') }} </button> </form> "},334:function(e,s){e.exports=' <form role=form class="clearfix animated" @submit.prevent=submit> <div class=form-group> <label :for=id>{{ _(\'Comment\') }}</label> <textarea v-el:textarea :id=id v-model=comment class=form-control rows=3 required></textarea> </div> <button type=submit :disabled="this.sending || !this.comment" class="btn btn-primary btn-block pull-right submit-new-message"> {{ _(\'Submit your comment\') }} </button> </form> '},335:function(e,s){e.exports=' <div class="discussion-thread panel panel-default" _v-67a4da23=""> <div class=panel-heading @click=toggleDiscussions _v-67a4da23=""> <div _v-67a4da23=""> <a href="#{{ discussionIdAttr }}" class=pull-right v-on:click.stop="" _v-67a4da23=""><span class="fa fa-link" _v-67a4da23=""></span></a> <strong _v-67a4da23="">{{ discussion.title }}</strong> <span class="label label-warning" v-if=discussion.closed _v-67a4da23=""><i class="fa fa-minus-circle" aria-hidden=true _v-67a4da23=""></i> {{ _(\'closed discussion\') }}</span> </div> </div> <div class=list-group v-show=detailed _v-67a4da23=""> <thread-message v-for="(index, response) in discussion.discussion" id="{{ discussionIdAttr }}-{{ index }}" :discussion=discussionIdAttr :index=index :message=response class=list-group-item _v-67a4da23=""> </thread-message></div> <div class=add-comment v-show="detailed &amp;&amp; !discussion.closed" _v-67a4da23=""> <button v-show="!formDisplayed &amp;&amp; detailed &amp;&amp; !discussion.closed" type=button class="btn btn-primary" @click=displayForm _v-67a4da23=""> {{ _(\'Add a comment\') }} </button> <div v-el:form="" id="{{ discussionIdAttr }}-new-comment" v-show="formDisplayed &amp;&amp; currentUser" class="animated form" _v-67a4da23=""> <thread-form v-ref:form="" :discussion-id=discussion.id _v-67a4da23=""></thread-form> </div> </div> <div class="panel-footer read-more" v-show=!detailed @click=toggleDiscussions _v-67a4da23=""> <span class=text-muted _v-67a4da23="">{{ discussion.discussion.length }} {{ _(\'messages\') }}</span> </div> <div class=panel-footer v-if=discussion.closed _v-67a4da23=""> <div class=text-muted _v-67a4da23=""> {{ _(\'Discussion has been closed\') }} <span v-if=discussion.closed_by _v-67a4da23=""> {{ _(\'by\') }} <a href="{{ discussion.closed_by.page }}" _v-67a4da23="">{{ discussion.closed_by | display }}</a> </span> {{ _(\'on\') }} {{ closedDate }} </div> </div> </div> '},336:function(e,s){e.exports=' <div class=discussion-threads _v-debbe940=""> <div class=control _v-debbe940=""> <pagination-widget :p=p class=pagination _v-debbe940=""> </pagination-widget> <div class=sort v-show="discussions.length > 1" _v-debbe940=""> <div class=btn-group _v-debbe940=""> <button class="btn btn-default btn-sm dropdown-toogle" type=button data-toggle=dropdown aria-haspopup=true aria-expanded=false _v-debbe940=""> {{ _(\'sort by\') }} <span class=caret _v-debbe940=""></span> </button> <ul class="dropdown-menu dropdown-menu-right" _v-debbe940=""> <li _v-debbe940=""><a class=by_created @click="sortBy(\'created\')" _v-debbe940="">{{ _(\'topic creation\') }}</a></li> <li _v-debbe940=""><a class=last_response @click="sortBy(\'response\')" _v-debbe940="">{{ _(\'last response\') }}</a></li> </ul> </div> </div> </div> <div class=loading v-if=loading _v-debbe940=""> <i class="fa fa-spinner fa-pulse fa-2x fa-fw" _v-debbe940=""></i> <span class=sr-only _v-debbe940="">{{ _(\'Loading\') }}...</span> </div> <discussion-thread v-ref:threads="" v-for="discussion in discussions" :discussion=discussion id="discussion-{{ discussion.id }}" track-by=id _v-debbe940=""> </discussion-thread> <a class="card discussion-card add" @click=displayForm v-show=!formDisplayed _v-debbe940=""> <div class=card-logo _v-debbe940=""><span _v-debbe940="">+</span></div> <div class=card-body _v-debbe940=""> <h4 _v-debbe940="">{{ _(\'Start a new discussion\') }}</h4> </div> </a> <div v-el:form="" id=discussion-create v-show=formDisplayed v-if=currentUser class="create list-group-item animated" _v-debbe940=""> <div _v-debbe940=""> <div class=avatar _v-debbe940=""> <avatar :user=currentUser _v-debbe940=""></avatar> </div> <div class=control _v-debbe940=""> <a href=#discussion-create _v-debbe940=""><span class="fa fa-link" _v-debbe940=""></span></a> <a @click=hideForm _v-debbe940=""><span class="fa fa-times" _v-debbe940=""></span></a> </div> <div _v-debbe940=""> <h4 class=list-group-item-heading _v-debbe940=""> {{ _(\'Starting a new discussion thread\') }} </h4> <p class=list-group-item-text _v-debbe940=""> {{ _("You\'re about to start a new discussion thread. Make sure that a thread about the same topic doesn\'t exist yet just above.") }} </p> </div> </div> <thread-form-create v-ref:form="" :subject-id=subjectId :subject-class=subjectClass _v-debbe940=""></thread-form-create> </div> </div> '},338:function(e,s,t){var i,a;t(345),i=t(308),a=t(331),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},339:function(e,s,t){var i,a;t(346),i=t(309),a=t(332),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},340:function(e,s,t){var i,a;i=t(310),a=t(333),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},341:function(e,s,t){var i,a;i=t(311),a=t(334),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},342:function(e,s,t){var i,a;t(347),i=t(312),a=t(335),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},343:function(e,s,t){var i,a;t(348),i=t(313),a=t(336),e.exports=i||{},e.exports.__esModule&&(e.exports=e.exports.default),a&&(("function"==typeof e.exports?e.exports.options||(e.exports.options={}):e.exports).template=a)},345:function(e,s,t){var i=t(324);"string"==typeof i&&(i=[[e.id,i,""]]);t(9)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},346:function(e,s,t){var i=t(325);"string"==typeof i&&(i=[[e.id,i,""]]);t(9)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},347:function(e,s,t){var i=t(326);"string"==typeof i&&(i=[[e.id,i,""]]);t(9)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},348:function(e,s,t){var i=t(327);"string"==typeof i&&(i=[[e.id,i,""]]);t(9)(i,{sourceMap:!0});i.locals&&(e.exports=i.locals)},965:966});
//# sourceMappingURL=post.3c8b9e59be816cbec542.js.map