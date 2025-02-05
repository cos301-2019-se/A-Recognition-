import { Component, OnInit } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AuthService} from '../auth.service';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-tab1',
  templateUrl: 'tab1.page.html',
  styleUrls: ['tab1.page.scss']
})
export class Tab1Page implements OnInit {

  public eventList: any;
  public message: any = '';
  public eventID: any;
  public valid : any;
  ngOnInit()
  {
    this.auth.getList().then( (res) =>
    {
      this.eventList = res;
    }).catch( (err) =>
    {
      console.log('An error has occurred', err);
    });
  }
  constructor(public auth: AuthService, private alertController: AlertController)
  { 
  }
    /** 
 * Function Name:presentAlert
 * Version: V3.5
 * Author: Richard McFadden
 * Funtional description: showcases the alerts
*/ 
  async presentAlert() {
    const alert = await this.alertController.create({
      header: 'OTP Access',
      message: this.message,
      buttons: ['OK']
    });

    await alert.present();
  }
  /** 
 * Function Name:setEventID
 * Version: V3.5
 * Author: Richard McFadden
 * Funtional description: gets the eventID from the selectBOXES
*/
  public setEventID(eventid: any)
  {
    this.eventID = eventid;
   // console.log(this.eventID.detail.value);
  }  
/** 
  * Function Name:vaidateOTP
  * Version: V3.5
  * Author: Richard McFadden
  * Funtional description: checks whether the otp matches based on the evnt id
  */
  public validateOTP(otp: any)
  {
    this.auth.validateOneTimePin(this.eventID.detail.value, otp).then( (data) =>
    {
      console.log(data);
      if(data == true){
        
        this.message = 'You are allowed access to the room now!';
        this.valid = true;
      }
      else
      {
        this.message = 'Either the OTP entered is wrong, expired or you are not allowed in right now.';
        this.valid = false;
      }
      this.presentAlert();
    });
  }

}
