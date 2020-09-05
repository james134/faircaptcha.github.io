(function(n){var e=function(){var i=arguments[0],t=[].slice.call(arguments,1);for(var n=0;n<t.length;++n){var r=t[n];for(key in r){var o=r[key];i[key]=typeof o==="object"?e(typeof i[key]==="object"?i[key]:{},o):o}}return i};var o={wav:"WebAudioRecorderWav.min.js",ogg:"WebAudioRecorderOgg.min.js",mp3:"WebAudioRecorderMp3.min.js"};var t={workerDir:"/",numChannels:2,encoding:"wav",options:{timeLimit:300,encodeAfterRecord:false,progressInterval:1e3,bufferSize:undefined,wav:{mimeType:"audio/wav"},ogg:{mimeType:"audio/ogg",quality:.5},mp3:{mimeType:"audio/mpeg",bitRate:160}}};var i=function(i,n){e(this,t,n||{});this.context=i.context;if(this.context.createScriptProcessor==null)this.context.createScriptProcessor=this.context.createJavaScriptNode;this.input=this.context.createGain();i.connect(this.input);this.buffer=[];this.initWorker()};e(i.prototype,{isRecording:function(){return this.processor!=null},setEncoding:function(e){if(this.isRecording())this.error("setEncoding: cannot set encoding during recording");else if(this.encoding!==e){this.encoding=e;this.initWorker()}},setOptions:function(i){if(this.isRecording())this.error("setOptions: cannot set options during recording");else{e(this.options,i);this.worker.postMessage({command:"options",options:this.options})}},startRecording:function(){if(this.isRecording())this.error("startRecording: previous recording is running");else{var i=this.numChannels,e=this.buffer,n=this.worker;this.processor=this.context.createScriptProcessor(this.options.bufferSize,this.numChannels,this.numChannels);this.input.connect(this.processor);this.processor.connect(this.context.destination);this.processor.onaudioprocess=function(t){for(var o=0;o<i;++o)e[o]=t.inputBuffer.getChannelData(o);n.postMessage({command:"record",buffer:e})};this.worker.postMessage({command:"start",bufferSize:this.processor.bufferSize});this.startTime=Date.now()}},recordingTime:function(){return this.isRecording()?(Date.now()-this.startTime)*.001:null},cancelRecording:function(){if(this.isRecording()){this.input.disconnect();this.processor.disconnect();delete this.processor;this.worker.postMessage({command:"cancel"})}else this.error("cancelRecording: no recording is running")},finishRecording:function(){if(this.isRecording()){this.input.disconnect();this.processor.disconnect();delete this.processor;this.worker.postMessage({command:"finish"})}else this.error("finishRecording: no recording is running")},cancelEncoding:function(){if(this.options.encodeAfterRecord)if(this.isRecording())this.error("cancelEncoding: recording is not finished");else{this.onEncodingCanceled(this);this.initWorker()}else this.error("cancelEncoding: invalid method call")},initWorker:function(){if(this.worker!=null)this.worker.terminate();this.onEncoderLoading(this,this.encoding);this.worker=new Worker(this.workerDir+o[this.encoding]);var e=this;this.worker.onmessage=function(n){var i=n.data;switch(i.command){case"loaded":e.onEncoderLoaded(e,e.encoding);break;case"timeout":e.onTimeout(e);break;case"progress":e.onEncodingProgress(e,i.progress);break;case"complete":e.onComplete(e,i.blob);break;case"error":e.error(i.message)}};this.worker.postMessage({command:"init",config:{sampleRate:this.context.sampleRate,numChannels:this.numChannels},options:this.options})},error:function(e){this.onError(this,"WebAudioRecorder.min.js:"+e)},onEncoderLoading:function(e,i){},onEncoderLoaded:function(e,i){},onTimeout:function(e){e.finishRecording()},onEncodingProgress:function(e,i){},onEncodingCanceled:function(e){},onComplete:function(e,i){e.onError(e,"WebAudioRecorder.min.js: You must override .onComplete event")},onError:function(i,e){console.log(e)}});n.WebAudioRecorder=i})(window);

//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var recorder; 						//WebAudioRecorder object
var input; 							//MediaStreamAudioSourceNode  we'll be recording
var encodingType = "wav"; 			//wav / ogg / mp3
var encodeAfterRecord = true;       // when to encode

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

var afrocaptcha_steps = 0; //mic not authorized
var afrocaptcha_icon = document.getElementById("afrocaptcha_icon");
var afrocaptcha_text = document.getElementById("afrocaptcha_text");
var afrocaptcha_slider = document.getElementById("afrocaptcha_slider");

function afrocaptcha_nopropagate(event){
   var e = event || window.event;
    if(e){
        e.preventDefault && e.preventDefault();
        e.stopPropagation && e.stopPropagation();
        e.cancelBubble = true;
        e.returnValue = false;
    }
}

function afrocaptcha_start(event) {
    afrocaptcha_nopropagate(event);
    
	__log("start called");

	/*
		Simple constraints object, for more advanced features see
		https://addpipe.com/blog/audio-constraints-getusermedia/
	*/
    
    var constraints = { audio: {channelCount: 1}, video:false }

    /*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
	    if (++afrocaptcha_steps == 1) { //step1 => mic authorized, no stream yet
	        //slide
	        console.log('sliding');
	        end_icon_left = afrocaptcha_slider.offsetWidth - 45;
	        num_steps = 10;
	        diff = Math.round((end_icon_left - 5)/num_steps);
	        tmp = 5; //start
	        time = 0;
	        
	        afrocaptcha_icon.style.fill="white";
	        afrocaptcha_icon.style.borderColor="white"
	        afrocaptcha_slider.children[0].style.background="#00c9a7";
	        afrocaptcha_text.style.visibility="hidden";
	        afrocaptcha_text.style.color="white";
	        
	        do {
	            tmp = Math.min(tmp+diff, end_icon_left);
	            setTimeout("afrocaptcha_icon.style.left='"+tmp+".px';afrocaptcha_slider.children[0].style.width='"+(tmp+45)+".px';", time+=20);
	        } while (tmp < end_icon_left);
	        tmp+=45
	        do {
	            tmp+=diff
	            setTimeout("afrocaptcha_slider.children[0].style.width='"+tmp+".px';", time+=20);
	        } while (tmp < (afrocaptcha_slider.offsetWidth+25));
	        setTimeout("afrocaptcha_text.style.visibility='visible';", time);
	        
	        afrocaptcha_text.innerHTML = "Hold to record";
	        return;
	    }
	    
		__log("getUserMedia() success, stream created, initializing WebAudioRecorder...");
		
		afrocaptcha_text.innerHTML = "Recording ...";

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext({sampleRate:8000});

		//update the format 
		__log("recording "+encodingType+" @ "+audioContext.sampleRate/1000+"kHz")

		//assign to gumStream for later use
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);
		
		//stop the input from playing back through the speakers
		//input.connect(audioContext.destination)

		recorder = new WebAudioRecorder(input, {
		  workerDir: "demo/", // must end with slash
		  encoding: encodingType,
		  numChannels:2, //2 is the default, mp3 encoding supports only 2
		  onEncoderLoading: function(recorder, encoding) {
		    // show "loading encoder..." display
		    __log("Loading "+encoding+" encoder...");
		  },
		  onEncoderLoaded: function(recorder, encoding) {
		    // hide "loading encoder..." display
		    __log(encoding+" encoder loaded");
		  }
		});

		recorder.onComplete = function(recorder, blob) { 
			__log("Encoding complete");
			createDownloadLink(blob,recorder.encoding);
		}

		recorder.setOptions({
		  timeLimit:120,
		  encodeAfterRecord:encodeAfterRecord,
	      ogg: {quality: 0.5},
	      mp3: {bitRate: 160}
	    });

		//start the recording process
		recorder.startRecording();

		 __log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUSerMedia() fails

	});

	//disable the record button
	/*
    recordButton.disabled = true;
    stopButton.disabled = false;
    */
    
    return false;
}

function afrocaptcha_stop(event) {
    afrocaptcha_nopropagate(event);
    
    if (afrocaptcha_steps == 1) {
        return;
    }
	__log("stop called");
	
	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

    afrocaptcha_text.innerHTML = "Hold icon to record";
	
	//tell the recorder to finish the recording (stop recording + encode the recorded audio)
	recorder.finishRecording();

	__log('Recording stopped');
}

afrocaptcha_icon.ontouchstart =
afrocaptcha_icon.onmousedown = afrocaptcha_start;
afrocaptcha_icon.ontouchend =
afrocaptcha_icon.onmouseup = afrocaptcha_stop;

function createDownloadLink(blob,encoding) {
	
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var link = document.createElement('a');

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//link the a element to the blob
	link.href = url;
	link.download = new Date().toISOString() + '.'+encoding;
	link.innerHTML = link.download;

	document.body.appendChild(au);
	document.body.appendChild(link);
}



//helper function
function __log(e, data) {
	console.log('afrocaptcha: ' + e + " " + (data || ''));
}