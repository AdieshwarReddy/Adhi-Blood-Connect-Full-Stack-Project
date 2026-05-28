export const BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"] as const;
export type BloodGroup = (typeof BLOOD_GROUPS)[number];

export interface Donor {
  id: string;
  name: string;
  bloodGroup: BloodGroup;
  city: string;
  distanceKm: number;
  available: boolean;
  reliability: number;
  lastDonation: string;
  phone: string;
}

export interface EmergencyRequest {
  id: string;
  patient: string;
  bloodGroup: BloodGroup;
  units: number;
  hospital: string;
  urgency: "Critical" | "High" | "Moderate";
  contact: string;
  city: string;
  createdAt: string;
}

export interface Notification {
  id: string;
  title: string;
  body: string;
  time: string;
  type: "emergency" | "info" | "success";
  read?: boolean;
}

export const dummyDonors: Donor[] = [
  { id: "d1", name: "Arjun Kumar", bloodGroup: "O+", city: "Bangalore", distanceKm: 2.4, available: true, reliability: 96, lastDonation: "2025-02-12", phone: "+91 98765 43210" },
  { id: "d2", name: "Priya Sharma", bloodGroup: "A+", city: "Bangalore", distanceKm: 4.1, available: true, reliability: 92, lastDonation: "2024-11-08", phone: "+91 98765 11122" },
  { id: "d3", name: "Rahul Verma", bloodGroup: "B+", city: "Mumbai", distanceKm: 1.8, available: false, reliability: 88, lastDonation: "2025-04-22", phone: "+91 98765 33344" },
  { id: "d4", name: "Sneha Iyer", bloodGroup: "AB-", city: "Chennai", distanceKm: 6.7, available: true, reliability: 99, lastDonation: "2024-09-30", phone: "+91 98765 55566" },
  { id: "d5", name: "Vikram Singh", bloodGroup: "O-", city: "Delhi", distanceKm: 3.2, available: true, reliability: 94, lastDonation: "2025-01-15", phone: "+91 98765 77788" },
  { id: "d6", name: "Anita Reddy", bloodGroup: "A-", city: "Hyderabad", distanceKm: 5.5, available: true, reliability: 90, lastDonation: "2024-12-20", phone: "+91 98765 99900" },
  { id: "d7", name: "Karthik Menon", bloodGroup: "B-", city: "Bangalore", distanceKm: 7.2, available: false, reliability: 85, lastDonation: "2025-03-05", phone: "+91 98765 12121" },
  { id: "d8", name: "Divya Nair", bloodGroup: "AB+", city: "Kochi", distanceKm: 8.9, available: true, reliability: 97, lastDonation: "2024-10-18", phone: "+91 98765 34343" },
];

export const dummyRequests: EmergencyRequest[] = [
  { id: "r1", patient: "Ramesh Gupta", bloodGroup: "O+", units: 3, hospital: "Apollo Hospital", urgency: "Critical", contact: "+91 99887 11223", city: "Bangalore", createdAt: "2 mins ago" },
  { id: "r2", patient: "Meera Joshi", bloodGroup: "A-", units: 2, hospital: "Fortis", urgency: "High", contact: "+91 99887 44556", city: "Bangalore", createdAt: "15 mins ago" },
  { id: "r3", patient: "Sanjay Patel", bloodGroup: "B+", units: 1, hospital: "Manipal", urgency: "Moderate", contact: "+91 99887 77889", city: "Mumbai", createdAt: "1 hour ago" },
  { id: "r4", patient: "Lakshmi Devi", bloodGroup: "AB+", units: 4, hospital: "AIIMS", urgency: "Critical", contact: "+91 99887 99001", city: "Delhi", createdAt: "3 hours ago" },
];

export const dummyNotifications: Notification[] = [
  { id: "n1", title: "Critical: O+ needed", body: "Apollo Hospital, Bangalore — 3 units", time: "2m", type: "emergency" },
  { id: "n2", title: "Donation reminder", body: "You're eligible to donate again", time: "1h", type: "info" },
  { id: "n3", title: "Thank you!", body: "Your last donation saved 3 lives", time: "2d", type: "success" },
];

export const adminStats = {
  totalDonors: 12847,
  activeRequests: 184,
  livesSaved: 38421,
  hospitalsPartner: 256,
  bloodGroupDistribution: [
    { group: "O+", value: 38 },
    { group: "A+", value: 27 },
    { group: "B+", value: 21 },
    { group: "AB+", value: 6 },
    { group: "O-", value: 4 },
    { group: "A-", value: 2 },
    { group: "B-", value: 1.5 },
    { group: "AB-", value: 0.5 },
  ],
  recentActivities: [
    { id: "a1", text: "New donor registered in Bangalore", time: "1m ago" },
    { id: "a2", text: "Emergency request fulfilled at Apollo", time: "12m ago" },
    { id: "a3", text: "Hospital onboarded: Manipal Mumbai", time: "1h ago" },
    { id: "a4", text: "85 donors notified for O- request", time: "2h ago" },
  ],
};
