import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Loading, Input, PageHeader, Badge } from '../components';
import { useAuth } from '../context';
import { userService } from '../services';
import { formatDate } from '../utils';

export default function Profile() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({});

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const data = await userService.getProfile();
        setProfile(data);
        setEditData(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Failed to load profile', error);
        setIsLoading(false);
      }
    };

    loadProfile();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  const handleEditChange = (e) => {
    const { name, value } = e.target;
    setEditData(prev => ({ ...prev, [name]: value }));
  };

  const handleSaveProfile = async () => {
    try {
      const result = await userService.updateProfile(editData);
      if (result.success) {
        setProfile(result.user);
        setIsEditing(false);
      }
    } catch (error) {
      console.error('Failed to update profile', error);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Profile" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-2xl mx-auto px-4 sm:px-6 py-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Profile Header */}
        <div className="panel p-8 mb-6">
          <div className="flex items-center gap-6 mb-6">
            <div className="w-20 h-20 bg-amber-lime rounded-full flex items-center justify-center text-3xl text-bg font-bold shrink-0">
              {(profile?.name || 'D U').split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
            </div>
            <div className="min-w-0">
              {isEditing ? (
                <Input type="text" name="name" value={editData.name} onChange={handleEditChange} className="mb-2" />
              ) : (
                <h2 className="heading-3">{profile?.name}</h2>
              )}
              <p className="text-ink-muted text-sm">Member since {formatDate(profile?.createdAt)}</p>
            </div>
          </div>

          <div className="space-y-4 mb-6">
            <div className="pb-4 border-b border-line">
              <p className="text-xs text-ink-muted mb-2 uppercase font-semibold tracking-wider">Email</p>
              {isEditing ? (
                <Input type="email" name="email" value={editData.email} onChange={handleEditChange} />
              ) : (
                <p className="text-ink font-medium">{profile?.email}</p>
              )}
            </div>

            <div className="pb-4 border-b border-line">
              <p className="text-xs text-ink-muted mb-2 uppercase font-semibold tracking-wider">Phone</p>
              {isEditing ? (
                <Input type="tel" name="phone" value={editData.phone} onChange={handleEditChange} />
              ) : (
                <p className="text-ink font-medium font-figures">{profile?.phone}</p>
              )}
            </div>

            <div>
              <p className="text-xs text-ink-muted mb-2 uppercase font-semibold tracking-wider">Country</p>
              {isEditing ? (
                <Input type="text" name="country" value={editData.country} onChange={handleEditChange} />
              ) : (
                <p className="text-ink font-medium">{profile?.country}</p>
              )}
            </div>
          </div>

          <div className="flex gap-3">
            {isEditing ? (
              <>
                <Button onClick={handleSaveProfile} className="flex-1">Save Changes</Button>
                <Button
                  variant="secondary"
                  onClick={() => { setIsEditing(false); setEditData(profile); }}
                  className="flex-1"
                >
                  Cancel
                </Button>
              </>
            ) : (
              <Button onClick={() => setIsEditing(true)} variant="secondary" className="w-full">
                Edit Profile
              </Button>
            )}
          </div>
        </div>

        {/* KYC Status */}
        <div className="panel p-8 mb-6">
          <h2 className="heading-3 mb-6">KYC Verification</h2>
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold text-ink">Status</p>
              <p className="text-sm text-ink-soft mt-1">
                {profile?.kyc?.verified ? 'Your account is fully verified' : 'Verification in progress'}
              </p>
            </div>
            <Badge variant="success">{profile?.kyc?.level === 'tier2' ? 'Tier 2' : 'Tier 1'}</Badge>
          </div>
        </div>

        {/* Security */}
        <div className="panel p-8 mb-6">
          <h2 className="heading-3 mb-6">Security</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-4 border-b border-line">
              <div>
                <p className="font-semibold text-ink">Two-Factor Authentication</p>
                <p className="text-sm text-ink-soft mt-1">Add an extra layer of security</p>
              </div>
              <button className="text-amber hover:brightness-110 font-semibold text-sm">Enable</button>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-ink">Password</p>
                <p className="text-sm text-ink-soft mt-1">Last changed 30 days ago</p>
              </div>
              <button className="text-amber hover:brightness-110 font-semibold text-sm">Change</button>
            </div>
          </div>
        </div>

        <Button onClick={handleLogout} variant="danger" className="w-full" size="lg">
          Logout
        </Button>
      </motion.div>
    </div>
  );
}
