import React from 'react';
import { Entity } from '../types/graph';

interface EntityListProps {
  entities: Entity[];
  onEntityClick?: (entity: Entity) => void;
}

const EntityList: React.FC<EntityListProps> = ({ entities, onEntityClick }) => {
  const getEntityTypeColor = (type: Entity['type']) => {
    const colors = {
      person: 'bg-blue-100 text-blue-800',
      organization: 'bg-purple-100 text-purple-800',
      location: 'bg-green-100 text-green-800',
      date: 'bg-yellow-100 text-yellow-800',
      account: 'bg-pink-100 text-pink-800',
      phone: 'bg-orange-100 text-orange-800',
      other: 'bg-gray-100 text-gray-800',
    };
    return colors[type];
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      <h3 className="text-lg font-semibold mb-4">Detected Entities</h3>
      <div className="space-y-2">
        {entities.map((entity) => (
          <div
            key={entity.id}
            onClick={() => onEntityClick?.(entity)}
            className={`p-2 rounded-md cursor-pointer hover:opacity-80 transition-opacity flex items-center justify-between ${
              getEntityTypeColor(entity.type)
            }`}
          >
            <span>{entity.label}</span>
            {entity.isAnomaly && (
              <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full">
                Anomaly
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default EntityList;